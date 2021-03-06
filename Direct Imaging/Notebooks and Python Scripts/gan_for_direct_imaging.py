# -*- coding: utf-8 -*-
"""GAN_for_Direct_Imaging.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FXcDbHg4FOA4LR_bLzcHbe73PaXuoLaN
"""

import tensorflow as tf
import glob
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from tensorflow.keras import layers
import time
#tf.enable_eager_execution()
from PIL import Image
from astropy.io import fits
import glob
import scipy
from scipy import signal
import cv2


from IPython import display
class data_for_GAN():
    def __init__(self):
                
        self.train_images = []
        self.train_images_raw=[]
        itera=0
        for filename in glob.glob('Artificial-Intelligence//Direct Imaging//Data//comtemp_flats-DD2//temp//*.fits'):
            #print('alpha')
            #fits.info(filename)
            self.train_images_raw.append(fits.getdata(filename))
               
            
            itera=itera+1
            if itera%100==0:
                print(iter)
        train_images = (np.array(self.train_images_raw) - 127.5) / 127.5
        print(np.shape(train_images))
        for ite in range(0,len(train_images)):
            custom_image_data=self.crop_custom(np.squeeze(train_images[ite,:,:]))
            if np.min(custom_image_data)!=np.max(custom_image_data): 
               self.train_images.append(custom_image_data)
               plt.imshow(custom_image_data)
               plt.axis('off')
               fig_name='Artificial-Intelligence//Direct Imaging//Data//comtemp_flats-DD2//temp//non_planetary_image_data//image_'+str(ite)+'_'+'.png'
               plt.savefig(fig_name)
               plt.close()
        
        for ite in range(0,len(self.train_images)):
            theta=np.int(np.round(np.random.randint(0,180),2))
            self.planetary_injection(self.train_images[ite],theta,ite)  
        self.planetary_image_data=[]
        itera=0
        '''
        for filename in glob.glob('Artificial-Intelligence//Direct Imaging//Data//comtemp_flats-DD2//temp//planetary_image_data//*.png'):
            
            planetary_images_raw = cv2.imread(filename)
            planetary_images_raw_crop = cv2.resize(planetary_images_raw, dsize=(28,28), interpolation=cv2.INTER_CUBIC)
            planetary_image = (np.array(planetary_images_raw_crop) - 127.5) / 127.5
            self.planetary_image_data.append(planetary_image)
            #print(itera)
            itera=itera+1
        '''
        
    def planetary_injection(self,image,theta,ite):
        im=self.gkern(10)
        fig=plt.figure(figsize=(10,10))
        plt.axis('off')
        rad=0.3
        plt.imshow(image)
        Px=0.5+rad*np.cos(theta*np.pi/180)
        Py=0.5+rad*np.sin(theta*np.pi/180)
        #print(Px,Py)
        newax = fig.add_axes([Px,Py, 0.02, 0.02])
        newax.imshow((im),interpolation='none')
        newax.axis('off')
        fig_name='Artificial-Intelligence//Direct Imaging//Data//comtemp_flats-DD2//temp//planetary_image_data//image_'+str(ite)+'_'+'.png'
        plt.savefig(fig_name)
        #print(ite)
        plt.close()
      
    def gkern(self,kernlen=21, std=3):
        """Returns a 2D Gaussian kernel array."""
        #print('#')
        gkern1d = signal.gaussian(kernlen, std=std).reshape(kernlen, 1)
        gkern2d = np.outer(gkern1d, gkern1d)
        return gkern2d

       

    def crop_custom(self,image,resize_w=28):
        
        i = int(73-32)
        j = int(212-32)
        crop_h=64
        crop_w=64
        
        New_Image=Image.fromarray(image[j:j+crop_h, i:i+crop_w]).resize(size=[resize_w, resize_w])
        New_Image_Conversion=New_Image.convert('L')
        return np.asarray(New_Image_Conversion)
        
class GAN():
    def __init__(self,obj):
        super().__init__()
        self.cross_entropy=tf.keras.losses.BinaryCrossentropy(from_logits=True)
        self.generator_optimizer = tf.keras.optimizers.Adam(1e-4)
        self.discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)
        self.BUFFER_SIZE = 100
        self.BATCH_SIZE = 25
        self.EPOCHS = 15000
        self.noise_dim = 100
        self.num_examples_to_generate = 16
        self.seed = tf.random.normal([self.num_examples_to_generate, self.noise_dim])
        self.train_dataset = tf.data.Dataset.from_tensor_slices(obj.train_images).shuffle(self.BUFFER_SIZE).batch(self.BATCH_SIZE)

        self.generator=self.make_generator_model()
        self.discriminator=self.make_discriminator_model() 
    
    def make_generator_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(7*7*64, use_bias=False, input_shape=(100,)))
        model.add(layers.BatchNormalization())
        model.add(layers.LeakyReLU())

        model.add(layers.Reshape((7,7, 64)))
        assert model.output_shape == (None, 7, 7, 64) # Note: None is the batch size

        model.add(layers.Conv2DTranspose(32, (5, 5), strides=(1, 1), padding='same', use_bias=False))
        assert model.output_shape == (None, 7, 7, 32)
        model.add(layers.BatchNormalization())
        model.add(layers.LeakyReLU())

        model.add(layers.Conv2DTranspose(16, (5, 5), strides=(2, 2), padding='same', use_bias=False))
        assert model.output_shape == (None, 14, 14, 16)
        model.add(layers.BatchNormalization())
        model.add(layers.LeakyReLU())

        #model.add(layers.Conv2DTranspose(1, (5, 5), strides=(4, 4), padding='same', use_bias=False))
        #assert model.output_shape == (None, 28, 28, 1)
        model.add(layers.Conv2DTranspose(1, (2, 2), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))

        return model
    
    def make_discriminator_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Conv2D(32, (5, 5), strides=(2, 2), padding='same',
                                         input_shape=[28, 28, 1]))
        model.add(layers.LeakyReLU())
        model.add(layers.Dropout(0.3))

        model.add(layers.Conv2D(16, (5, 5), strides=(2, 2), padding='same'))
        model.add(layers.LeakyReLU())
        model.add(layers.Dropout(0.3))

        #model.add(layers.Conv2D(16, (5, 5), strides=(4, 4), padding='same'))
        #model.add(layers.LeakyReLU())
        #model.add(layers.Dropout(0.3))

        

        model.add(layers.Flatten())
        model.add(layers.Dense(1))

        return model
    
    def discriminator_loss(self,real_output, fake_output):
        real_loss = self.cross_entropy(tf.ones_like(real_output), real_output)
        fake_loss = self.cross_entropy(tf.zeros_like(fake_output), fake_output)
        total_loss = real_loss + fake_loss
        return total_loss

    def generator_loss(self,fake_output):
        return self.cross_entropy(tf.ones_like(fake_output), fake_output)
    
    #@tf.function
    def train_step(self,images):
        noise = tf.random.normal([self.BATCH_SIZE, self.noise_dim])

        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
          generated_images = self.generator(noise, training=True)

          real_output = self.discriminator(images, training=True)
          fake_output = self.discriminator(generated_images, training=True)

          gen_loss = self.generator_loss(fake_output)
          disc_loss = self.discriminator_loss(real_output, fake_output)

        gradients_of_generator = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)

        self.generator_optimizer = tf.keras.optimizers.Adam(1e-4)
        self.discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

        self.generator_optimizer.apply_gradients(zip(gradients_of_generator, self.generator.trainable_variables))
        self.discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, self.discriminator.trainable_variables))
    
    def generate_and_save_images(self,model, epoch, test_input):
        
        predictions = model(test_input, training=False)

        fig = plt.figure(figsize=(4,4))

        for i in range(predictions.shape[0]):
            plt.subplot(4, 4, i+1)
            plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5)
            plt.axis('off')

        plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
        plt.show()
    
    
    def center_crop_custom(x,resize_w=256):
        
        h, w = x.shape[:2]
        i = int(73-32)
        j = int(212-32)
        crop_h=64
        crop_w=64
        return scipy.misc.imresize(x[j:j+crop_h, i:i+crop_w],
                                  [resize_w, resize_w])

    def train(self):
          checkpoint = tf.train.Checkpoint(generator_optimizer=self.generator_optimizer,
                                 discriminator_optimizer=self.discriminator_optimizer,
                                 generator=self.generator,
                                 discriminator=self.discriminator)
          checkpoint_dir = './training_checkpoints'
          checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
          
          status = checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
          for epoch in range(self.EPOCHS):
            start = time.time()

            for image_batch in self.train_dataset:
                self.train_step(image_batch)

            # Produce images for the GIF as we go
                display.clear_output(wait=True)
                self.generate_and_save_images(self.generator,
                                         epoch + 1,
                                         self.seed)

            # Save the model every 15 epochs
            
            if (epoch + 1) % 15 == 0:
              checkpoint.save(file_prefix = checkpoint_prefix)
              print(epoch)

            
          display.clear_output(wait=True)
          
          self.generate_and_save_images(self.generator,
                                       epoch,
                                       self.seed)
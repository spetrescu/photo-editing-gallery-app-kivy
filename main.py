from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView 
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout 
from kivy.uix.dropdown import DropDown 
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import os
from os.path import join, dirname
from PIL import Image as pillow
import cv2 
import numpy as np

class ViewImage(ModalView):
    pass

class GalleryWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #self.images = self.get_imgs('imgs')
        #self.show_imgs(self.images)
        #print(self.get_imgs('imgs1'))
        #im = Image(source='imgs/rev.jpg')
        # print('Image Width:', im.texture_size[0])
        # print('Image Height:', im.texture_size[1])
        # print('Image Size:', im.texture_size)
        #self.add_widget(im)
        self.view_img_children = None

    def get_imgs(self, img_path):
        if not os.path.exists(img_path):
            print('Invalid Path...')
            return -1
        else:
            all_files = os.listdir(img_path)
            imgs = []
            for f in all_files:
                if f.endswith('.png') or f.endswith('.PNG') or f.endswith('.JPG') or f.endswith('.jpg') or f.endswith('.JPEG') or f.endswith('.jpeg'):
                    imgs.append('/'.join([img_path, f]))
            return imgs

    def show_imgs(self, imgs):
        base = self.ids.img_base
        base_data = []
        for img in imgs:
            im_name = img[img.rfind('/')+1:]
            if len(im_name) > 20:
                im_name = im_name[:18] + '...'
            base_data.append({'im_source':img, 'im_caption': im_name})
            #base_data.append({'source':img})
        base.data = base_data

    def get_image(self, im_path):
        self.ids.img_base.data = []
        self.images = [im_path]
        self.show_imgs(self.images)
        self.ids.scrn_mngr.current = 'scrn_media'
        self.ids.scrn_open.trigger = ''
    def get_folder(self, im_path):
        self.ids.img_base.data = []
        self.images = self.get_imgs(im_path)
        self.show_imgs(self.images)
        self.ids.scrn_mngr.current = 'scrn_media'

    def next_image(self, inst):
        images = self.images
        cur_idx = None
        last_idx = len(images) -1
        view_children = inst.parent.parent.parent.children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source

        for i, img in enumerate(images):
            if img == cur_img:
                cur_idx = i 

        if cur_idx != last_idx:
            nxt_img = images[cur_idx+1]
        else:
            nxt_img = images[0]

        image_container.source = nxt_img

    def prev_image(self, inst):
        images = self.images
        cur_idx = None
        last_idx = len(images) -1
        view_children = inst.parent.parent.parent.children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source

        for i, img in enumerate(images):
            if img == cur_img:
                cur_idx = i 

        if cur_idx != 0:
            prev_img = images[cur_idx-1]
        else:
            prev_img = images[last_idx]

        image_container.source = prev_img
        #print(inst.parent)

    def new_img_name(self, inst):
        view_children = inst.parent.parent.parent.children
        self.view_img_children = view_children
        new_name = TextInput(hint_text='New Image Name', multiline=False)
        new_name.bind(on_text_validate=self.rename_img)

        new_name_modal = ViewImage(size_hint=(None, None), size=(400, 50))
        new_name_modal.add_widget(new_name)
        new_name_modal.open()

    def rename_img(self, inst):
        inst.parent.dismiss()
        new_name = inst.text
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
        ext = cur_img[cur_img.rfind('.'):]

        try:
            im_path = cur_img[:cur_img.rfind('/')+1]
            os.rename(cur_img, im_path+new_name+ext)
            self.ids.img_base.data = []
            images = self.get_imgs('imgs')
            self.show_imgs(images)
            return True
        except Exception as e:
            print(e)
            return False

    def callback1(self, inst):
        self.text1=self.txt_1.text
        return self.text1

    def callback2(self, inst):
        self.text2=self.txt_2.text
        return self.text2

    def viewimg(self, instance):
        #print(instance.im_source)
        im = Image(source=instance.im_source)
        view_size = self.img_resize(im)

        effects_drop = DropDown()

        btn_prev = Button(text='Prev', size_hint_y=None, height = 50)
        btn_prev.bind(on_release=self.prev_image)
        btn_rename = Button(text='Rename', size_hint_y=None, height = 50)
        btn_rename.bind(on_release=self.new_img_name)
        btn_effects = Button(text='Effects', size_hint_y=None, height = 50)
        btn_effects.bind(on_release=effects_drop.open)
        btn_next = Button(text='Next', size_hint_y=None, height = 50)
        btn_next.bind(on_release=self.next_image)

        btn_black = Button(text='Grayscale', size_hint_y=None, height = 50)
        btn_black.bind(on_release=self.black_image)
        btn_bin = Button(text='Binarization', size_hint_y=None, height = 50)
        btn_bin.bind(on_release=self.bin_image)

        self.txt_1 = TextInput(hint_text='min', size_hint_y=None, height = 50, multiline = False)
        #btn_1.bind(on_release=self.callback)
        self.txt_1.bind(on_text_validate=self.callback1)
        self.txt_2 = TextInput(hint_text='max', size_hint_y=None, height = 50, multiline = False)
        #btn_bin.bind(on_release=self.bin_image)
        self.txt_2.bind(on_text_validate=self.callback2)

        effects_drop.add_widget(btn_black)
        effects_drop.add_widget(btn_bin)
        effects_drop.add_widget(self.txt_1)
        effects_drop.add_widget(self.txt_2)
        

        image_ops = BoxLayout(size_hint=(None, None), size=(400, 30), spacing=4)
        image_ops.add_widget(btn_prev)
        image_ops.add_widget(btn_rename)
        image_ops.add_widget(btn_effects)
        image_ops.add_widget(btn_next)
        anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        anchor.add_widget(image_ops)
        image_container = BoxLayout()

        view = ViewImage(size_hint=(None,None),size=view_size)
        image_container.add_widget(im)
        view.add_widget(image_container)
        view.add_widget(anchor)
        view.open()
        self.view_img_children = view.children

    def black_image(self, inst):
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
        im = pillow.open(cur_img)

        # source = im.split()
        # R, G, B = 0, 1, 2
        # mask = source[R].point(lambda i: i < 100 and 255)
        # out = source[B].point(lambda i: i * 0.7)

        # source[G].paste(out, None, mask)
        #new_im = pillow.merge(im.mode, source)
        new_im = pillow.open(cur_img).convert('L')


        name = im.filename[:-4] + '_blackW' + im.filename[-4:]
        im_cap = im.filename[im.filename.rfind('/')+1:]
        new_im.save(name)

        self.ids.img_base.data.insert(0, {'im_source':name, 'im_caption':im_cap})
        self.ids.img_base.refresh_from_data()
        image_container.source = name

    def bin_image(self, inst):
        
        if self.txt_1.text == '' and self.txt_2.text=='':
            minimum_minimorum = 0
            maximum_maximorum = 255
        elif self.txt_1.text == '' and self.txt_2.text!='':
            minimum_minimorum = 0
            maximum_maximorum = int(self.txt_2.text)
        elif self.txt_1.text != '' and self.txt_2.text=='':
            minimum_minimorum = int(self.txt_1.text)
            maximum_maximorum = 255
        else:        
            minimum_minimorum = int(self.txt_1.text)
            maximum_maximorum = int(self.txt_2.text)
        # print(self.txt_1.text)
        
        # print(self.txt_2.text)
        
        view_children = self.view_img_children
        cur_img = None
        image_container = None

        for child in view_children:
            if str(child).find('BoxLayout') > -1:
                image_container = child.children[0]
                cur_img = image_container.source
        im = pillow.open(cur_img)

        open_cv_image = np.array(im)


        retval, threshold = cv2.threshold(open_cv_image, minimum_minimorum, maximum_maximorum, cv2.THRESH_BINARY)
        print(minimum_minimorum, maximum_maximorum)
        new_im = pillow.fromarray(threshold)

        name = im.filename[:-4] + '_bin' + im.filename[-4:]
        im_cap = im.filename[im.filename.rfind('/')+1:]
        new_im.save(name)

        self.ids.img_base.data.insert(0, {'im_source':name, 'im_caption':im_cap})
        self.ids.img_base.refresh_from_data()
        image_container.source = name


    def img_resize(self, img):
        im_size_x, im_size_y = img.texture_size
        ratio = im_size_x/im_size_y
        aspect = self.aspect_ratio(ratio, 50)

        while im_size_x >= Window.width or im_size_y >= Window.height:
            if im_size_x > im_size_y:
                im_size_x -= aspect[0]
                im_size_y -= aspect[1]
            else:
                im_size_y -= aspect[1]
        return [im_size_x, im_size_y]
    
    def aspect_ratio(self, val, lim):

        lower = [0, 1]
        upper = [1, 0]

        while True:
            mediant = [lower[0] + upper[0], lower[1] + upper[1]]

            if (val * mediant[1] > mediant[0]) :
                if (lim < mediant[1]) :
                    return upper
                lower = mediant
            elif (val * mediant[1] == mediant[0]) :
                if (lim >= mediant[1]) :
                    return mediant
                
                if (lower[1] < upper[1]) :
                    return lower
                
                return upper
            else :
                if (lim < mediant[1]) :
                    return lower
                
                upper = mediant
class GalleryApp(App):
    def build(self):
        
        return GalleryWindow()

if __name__=='__main__':
    GalleryApp().run()
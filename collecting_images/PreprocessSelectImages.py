from shutil import copyfile
import os
from glob import glob
from PIL import Image
from dealing_with_images import square_resize_image
from matplotlib.pyplot import imread
import image_embeddings
import ipywidgets as widgets
from functools import partial
from IPython.display import HTML, Image as Image1, display, clear_output

def has_transparency(img):
        if img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True
        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True

        return False

def create_buttons(curImgIdx):
    btns_names = ['Yes', 'No']
    for btn_name in btns_names:
        button_download = widgets.Button(description = btn_name)   
        button_download.on_click(partial(on_clicked, btn_label=btn_name, curImgIdx=curImgIdx))
        display(button_download)

def preprocess_select_images(dataset, base_images, base_images_dir, target_dir, create_embeddings = True):
    """
    Args:
    dataset - folder name of the location of images to check
    base_images - list of images to which the images should be similar to
    base_images_dir - the directory at which the base images are located at
    target_dir - the directory where to put selected images
    """
    from keras.preprocessing import image
    # Let's define some paths where to save images, tfrecords and embeddings
    path_images = f"{dataset}/images"
    path_tfrecords = f"{dataset}/tfrecords"
    path_embeddings = f"{dataset}/embeddings"
    
    if not os.path.exists(path_images):
        os.makedirs(path_images)
    
    # copying base_images
    for im_fn in base_images:
        copyfile(os.path.join(base_images_dir, im_fn), os.path.join(path_images, im_fn))
    
    # check if the image is transparent
    for im_fn in glob(f'{path_images}/*jpg'):
        with Image.open(im_fn) as im:
            if has_transparency(im) == True:
    #             display(Image1(im_fn))
                try:
                    print('deleted', im_fn)
                    os.remove(im_fn)
                except:
                    print('could not delete', im_fn)
    
    # loading as PIL objects
    maybe_eyes = []
    for p in glob(f'{path_images}/*jpg'):
        try:
            maybe_eyes.append(image.load_img(p))
        except UserWarning:
            print(p)
    
    # loading the filenames
    fns_to_check = glob(f'{path_images}/*jpg')
    # resizing to 224x224
    for imgId, img in enumerate(maybe_eyes):
        resized_img = square_resize_image(img, 224)
        resized_img.save(os.path.join(fns_to_check[imgId]))
    
    # removing images that are black and white
    for f_name in glob(f'{path_images}/*jpg'):
        image = imread(f_name)
        if len(image.shape)<3:
              colorType = 'gray'
        elif len(image.shape)==3:
              colorType = 'color'
        else:
              colorType = 'others'
        if colorType == 'gray':
#             display(Image1(f_name))
            os.remove(f_name)
    
    # converting .jpg to .jpeg
    for im_fn in glob(f'{path_images}/*jpg'):
        im = Image.open(im_fn)
        im.save(im_fn[:-4]+'.jpeg')
        os.remove(im_fn)
    
    if create_embeddings == True:
        # convert images to tfrecords
        image_embeddings.inference.write_tfrecord(image_folder=path_images,
                                              output_folder=path_tfrecords,
                                              num_shards=10)

        # create embeddings
        image_embeddings.inference.run_inference(tfrecords_folder=path_tfrecords,
                                             output_folder=path_embeddings,
                                             batch_size=1000)
    
    # create vector space with knn
    [id_to_name, name_to_id, embeddings] = image_embeddings.knn.read_embeddings(path_embeddings)
    index = image_embeddings.knn.build_index(embeddings)
    
    base_images_ids = tuple(
        idx for im_fn, idx in name_to_id.items() if im_fn+'.jpg' in base_images)
    print("base_images_ids", base_images_ids)
    
    # getting the knn distance of other images to base images
    [image_embeddings.knn.display_picture(path_images, id_to_name[img_fn]) for img_fn in base_images_ids]
    results = image_embeddings.knn.search(
        index, id_to_name, sum(embeddings[idx] for idx in base_images_ids), len(glob(f'{path_images}/*jpeg'))
    )
    
    print(len(fns_to_check))
    
    global on_clicked
    
    def on_clicked(arg, btn_label, curImgIdx):
#         target_dir = 'gettingMoreImages/normal_in_camera'
        img_fn = results[curImgIdx][1]
        if btn_label == 'Yes':
            copyfile(path_images+'/'+img_fn+'.jpeg', target_dir+'/'+img_fn+'.jpeg')

        clear_output(wait=True)

    #     print('btn_label', btn_label)
    #     print(path_images+'/'+img_fn+'.jpeg')
    #     print(target_dir+img_fn+'.jpeg')
        curImgIdx += 1
        img_fn = results[curImgIdx][1]
        print('current image index: ', curImgIdx)
        img = Image1(filename=path_images+'/'+img_fn+'.jpeg')
        display(img)

        create_buttons(curImgIdx)
    
    return results, path_images, on_clicked
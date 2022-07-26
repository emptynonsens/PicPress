import streamlit as st
from PIL import Image
from io import BytesIO

st.set_page_config(page_title = 'PicPress', layout='centered')

def load_image(image_file):
	img = Image.open(image_file)
	return img

def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def compress_download(img_file, quality_level, size_reduction_lvl, img_name, format_types):
	img = Image.open(img_file)
	#img_matrix = (np.asarray(img)/255)
	img = img.reduce(size_reduction_lvl)

	#compressed_image = Image.fromarray(X_reconstructed)
	#st.write('Image found with width: {}, height: {}, depth: {}'.format(w, h, d))
	#matrix = poolingOverlap(img_matrix, [3,3])
	#img_matrix = block_reduce(img_matrix, (2,2), np.max)
	#img_con = Image.fromarray(img_matrix, 'RGB')
	#st.image(img,width=250)
	#st.write(get_image_download_link(img, 'com
	buf = BytesIO()
	img.save(buf, format="JPEG", optimize = True, quality = quality_level )
	byte_im = buf.getvalue()
	return byte_im, img_name

types=["png","jpg","jpeg", "bmp"]
st.title("PicPress - compress your image")
image_file = st.file_uploader("Upload your image", type=types)

if image_file is not None:
	col1, col2 = st.columns([0.6, 0.4])
	
	file_details = {"filename":image_file.name, "filetype":image_file.type,
                    "filesize MB":image_file.size/1000000}
	img_core = image_file.name.split('.')[0]
	with col1:
		st.image(load_image(image_file),width=400)

	with col2:
		st.write(file_details)
		quality_level = st.slider('Select quality level %',1, 100, 30)
		size_reduction_lvl = st.slider('Select size reduction multiplier',1.0, 10.0, 1.0)

		if st.button(label='Compress'):
			st.session_state['byte_im'], st.session_state['img_name'] = compress_download(image_file,quality_level, size_reduction_lvl, img_core, types)
		else:
			pass

		if 'byte_im' in st.session_state:
			extenstion = st.selectbox('Choose output extension', types)
			st.download_button('Download', data = st.session_state['byte_im'], file_name = str(st.session_state['img_name'])+'.'+str(extenstion))


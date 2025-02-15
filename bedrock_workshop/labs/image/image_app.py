import streamlit as st
import image_lib as glib

st.set_page_config(layout = 'wide', page_title = 'Image Page') # đặt chiều rộng trang lớn hơn để phù hợp với các cột
st.title('Tạo hình ảnh')

col1, col2 = st.columns(2) # tạo 2 cột


# Cột 1, tạo multiline text box và button (input element)
with col1:
    st.subheader('Nhập mô tả hình ảnh') # Tiêu đề phụ cho cột 1
    prompt_text = st.text_area('Prompt Text', height = 200, label_visibility = 'collapsed')
    go_button = st.button('Gửi', type = 'primary')

# Cột 2, tạo ảnh lấy từ input cột 1
with col2:
    st.subheader('Kết quả: ')

    if go_button:
        with st.spinner('Đang vẽ ...'):
            generated_image = glib.get_image_response(prompt_content = prompt_text)
        st.image(generated_image)
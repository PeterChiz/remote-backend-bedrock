import streamlit as st
import text_lib as glib

st.set_page_config(page_title = 'Text Page')
st.title('Nhập câu hỏi:')

input_text = st.text_area('Input text', label_visibility = 'collapsed') # display a multiline text box with no label
go_button = st.button('Gửi', type = 'primary')

if go_button:
    with st.spinner('Đang tìm kiếm ... '): # Hiển thị biểu tượng tải (spinner) trong khi đoạn mã trong khối with đang chạy.
        response_content = glib.get_text_response(input_content=input_text)
        st.write(response_content) # = print(response_content)

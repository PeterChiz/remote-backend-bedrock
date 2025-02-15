import streamlit as st #all streamlit commands will be available through the "st" alias
# Add the page title and configuration.
# Setting the page title on the actual page and the title shown in the browser tab
st.set_page_config(page_title = "This is Peter's Streamlist")
st.title('Streamlit Page')
#Add the input elements.
##Creating an input text box and button to get a color from the user.
name_text = st.text_input("What's your name ?") # display a text box
go_button = st.button('Gửi', type='primary') # display a primary button
# Add the output elements.
## Use the if block below to handle the button click. 
## Then format the submitted color and display it using Streamlit's write function.
if go_button: #code in this if block will be run when the button is clicked
    st.write(f'Hello {name_text}')
import streamlit as st
import db_fun
from PIL import Image
import base64
from db_fun import *
import pandas as pd
st.set_option('deprecation.showPyplotGlobalUse',False)

#Layout templates
title_temp="""
<div style="background-color:grey;padding:10px,margin:10px;">
<h4 style="color:black;text-align:center;">Title:{}</h4>
<h4 style="color:black;text-align:center;">Author:{}</h4>
<h6 style="color:black;text-align:center;">Post Date:{}</h6>
<div style="text-align:center;">
<img src="data:image/jpg;base64,{}" alt="Image"
style='Horizontal-align:center' width="200px" height="200px">
</div>
<br/>
<br/>
<p style='text_align:justify'>{}</p>
</div>
"""
st.subheader("Blog Database Management Using Streamlit")
choice=st.sidebar.selectbox('Select Menu', ["Home","Add post", "Search","Manage Blog"])
db_fun.create_table()
if choice=="Home":
    result=db_fun.view_all_records()
    #st.write(result)
    for i in result:
        title=i[0]
        author=i[1]
        article=i[2]
        date=i[3]
        #open saved image after uploading
        try:
            b_image="%s.jpg" %author
            file=open(b_image,"rb").read()
            blog_image=base64.b64encode(file).decode("utf-8")
            file.close()
        except:
            print("couldn't open an image")
        st.markdown(title_temp.format(title,author,date,blog_image,article),unsafe_allow_html=True)

elif choice=="Add post":
    #st.write('Add post')
    blog_title=st.text_input("Enter the Title")
    blog_author=st.text_input("Enter the Author name")
    blog_article=st.text_area("Enter the article contents")
    blog_date=st.date_input("Enter the Published date")

    try:
        # upload the image
        img_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        image=Image.open(img_file)
        # Save an image to the folder
        image = image.convert('RGB')
        img = '{}.jpg'.format(blog_author)
        image.save(img)
        # Open a file in binary mode
        file = open(img, 'rb').read()
        # we must encode the file to get base64 string
        file = base64.b64encode(file)
    except:
        print("Error1: couldn't open image! Make sure the extension is correct")

    if st.button("Add Blog"):
        add_post(blog_title,blog_author,blog_article, blog_date, file)
        st.success(f"Successfully Add Blog a blog {blog_title}")
        #st.write("Add post")
elif choice=="Search":
    st.subheader("Search Articles")
    search_term=st.text_input("Enter the search term")
    choice=st.radio("Search article by fields",('Title','Author'))
    if (choice=='Title'):
        result=db_fun.get_blog_title(search_term)
        #st.write(result)
    if(choice=='Author'):
        result=db_fun.get_blog_author(search_term)
        #st.write(result)
    if st.button('search'):
        for i in result:
            title=i[0]
            author=i[1]
            article=i[2]
            date=i[3]
            #open saved image after uploading
            try:
                b_image="%s.jpg" %author
                file=open(b_image,"rb")
                image=base64.b64encode(file).decode("utf-8")
                file.close()
            except:
                print("couldn't open an image")
            st.markdown(title_temp.format(title,author,date,b_image,article),unsafe_allow_html=True)
elif choice=="Manage Blog":
    st.write("Manage Blog")
    data=view_all_records()
    #st.write(data)
    blog_table=pd.DataFrame(data,columns=['Title','Author','Article','Post Date','Author Image'])
    st.write(blog_table)
    delete_records=st.text_input('Enter Author Name')
    if st.button('Delete'):
        db_fun.delete_blog(delete_records)
        updated_data=view_all_records()
        blog_table = pd.DataFrame(updated_data, columns=['Title', 'Author', 'Article', 'Post Date', 'Author Image'])
        st.write(blog_table)
    st.subheader('Graphical Visualization')
    title_count=blog_table['Title'].value_counts()
    st.write(title_count)
    title_count.plot(kind='bar')
    st.pyplot()
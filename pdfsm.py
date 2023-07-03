import streamlit as st
import os
from PyPDF2 import PdfMerger
from PyPDF2 import PdfWriter, PdfReader

st.set_page_config(page_title='PDFmsX', page_icon='pdf.png', layout="centered", initial_sidebar_state="auto",
                   menu_items=None)

hide_streamlit_style = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def merge():
    def merge_pdfs(pdfs):
        merger = PdfMerger()

        for pdf in pdfs:
            merger.append(pdf)

        output_path = os.path.splitext(pdfs[0])[0] + "_merge.pdf"
        merger.write(output_path)
        merger.close()

        return output_path

    def main():
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>PDF "
            "Merger</h1></center>",
            unsafe_allow_html=True)

        uploaded_files = st.file_uploader("Upload Multiple PDF files", accept_multiple_files=True, type="pdf")

        if st.button("Merge PDFs"):
            if uploaded_files:
                pdf_paths = []
                for pdf_file in uploaded_files:
                    pdf_paths.append(pdf_file.name)
                    with open(pdf_file.name, "wb") as f:
                        f.write(pdf_file.getbuffer())

                merged_pdf_path = merge_pdfs(pdf_paths)
                st.success("PDFs merged successfully!")

                with open(merged_pdf_path, "rb") as f:
                    st.download_button(label="Download", data=f, file_name=os.path.basename(merged_pdf_path))

            else:
                st.warning("Please upload at least one PDF file.")

    if __name__ == "__main__":
        main()


def split():
    def split_pdf(pdf_path, start_page, end_page):

        pdf_reader = PdfReader(pdf_path)

        total_pages = len(pdf_reader.pages)

        if end_page > total_pages:
            st.warning("Invalid page number. The PDF contains fewer pages.")
            return None

        pdf_writer = PdfWriter()

        for page_number in range(start_page, end_page + 1):
            if page_number <= total_pages:
                pdf_writer.add_page(pdf_reader.pages[page_number - 1])

        output_path = os.path.splitext(os.path.basename(pdf_path))[0] + "_split.pdf"

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

        return output_path

    def main():
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>PDF Splitter</h1></center>",
            unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", key="fileUploader")

        if uploaded_file:
            pdf_path = uploaded_file.name
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            total_pages = len(PdfReader(pdf_path).pages)

            start_page = st.number_input("From page", value=1, min_value=1, max_value=total_pages, step=1)
            end_page = st.number_input("To page", value=total_pages, min_value=start_page, max_value=total_pages,
                                       step=1)

            if st.button("Split PDF"):
                output_path = split_pdf(pdf_path, start_page, end_page)
                if output_path:
                    st.success("PDF split successfully!")
                    with open(output_path, "rb") as f:
                        st.download_button(label="Download", data=f, file_name=os.path.basename(output_path))

    if __name__ == "__main__":
        main()


def main():
    st.sidebar.markdown(
        "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 24px;'>Merge and "
        "Split</h1></center>",
        unsafe_allow_html=True)
    st.sidebar.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu07FFtGLz9EV84QYqIrkwbS_AfdDLZaS75Sqj_Pls"
        "-oPaDX6UITS6OkKDAvML207ccwI&usqp=CAU",
        use_column_width=True)

    selected_sidebar = st.sidebar.radio("Please Select One", ["PDF Merge", "PDF Split"])

    if selected_sidebar == "PDF Merge":
        merge()
    elif selected_sidebar == "PDF Split":
        split()


if __name__ == "__main__":
    main()

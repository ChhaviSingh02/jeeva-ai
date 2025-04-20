#import necessary modules
import streamlit as st
import pathlib as path
import google.generativeai as genai
from io import BytesIO

from api_key import api_key

#CONFIGURE GENAI WITH API KEY
genai.configure(api_key=api_key)
#set up the model
# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
}
#apply safety settings not available in the gmeini studion rn,
#gotchu

#configure the model

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro-exp-03-25",  # Changed the model name here
    generation_config=generation_config,
)
system_prompt="""
    As a highly skilled medical practitioner specializing in image analysis, you are tasked with the examining medical images for  a renowned medical hospital. Your expertise is crucial in identifying , disease or health issues that may be present in the images.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate the observations in structured form
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain findings are "unable to be determined on the provided image".
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any medical decisions."
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis outlined above.

"""
#set the page conifguration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot")

#set the logo
st.image("jeeva.png",width=300)

#set the title
st.title("Jeeva Vital Image Analytics")
#set the subtitle
st.subheader("An application that can help users to identify medical iamges")

uploaded_file=st.file_uploader("Upload the medical image for analysis", type=["png","jpg","jpeg"])
if uploaded_file:
    st.image(uploaded_file,width=300, caption="Uploaded Mdeical Image")
#frontend is completed here,
#create the main logic form here and above

submit_button=st.button("Generate the analysis")
if submit_button and uploaded_file is not None:
    #process the uploaded image
    image_data = uploaded_file.getvalue()
    image_mime_type = uploaded_file.type

    #image parts
    image_part = {"mime_type": image_mime_type, "data": image_data}

    # Start the chat session with the user's input (image and system prompt)
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    image_part,
                    system_prompt,
                ],
            }
        ]
    )
    # Send the message to get the model's response
    response = chat_session.send_message("Analyze the uploaded medical image and provide your findings.")
    st.subheader("Analysis:")
    st.write(response.text)
elif submit_button:
    st.warning("Please upload a medical image for analysis.")

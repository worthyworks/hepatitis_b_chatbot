import streamlit as st
from fuzzywuzzy import fuzz
import smtplib
from email.message import EmailMessage


# Define CSS styles
st.markdown(
    """
    <style>
    .stApp {
        max-width: 800px;
        padding: 20px;
    }
    .st-eb {
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        background-color: #f5f5f5;
    }
    .stTextInput {
        max-width: 600px;
    }
    .stButton > button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define a dictionary of common questions and their answers
common_questions = {
    "What is hepatitis B?": "Hepatitis B is a viral infection that affects the liver. It can lead to acute and chronic liver disease.",
    "How is hepatitis b transmitted?": "There are several ways by which hepatitis B is transmitted - including via blood products, unprotected sexual activity with an infected person and use of unsterile sharps. Mother to child transmission is most common in developing countries.",
    "Why is hepatitis B so dangerous?": "Hepatitis B is dangerous because it can cause chronic liver inflammation, cirrhosis, and an increased risk of liver cancer.",
    "Is hepatitis B dangerous?": "Hepatitis B is dangerous because it can cause chronic liver inflammation, cirrhosis, and an increased risk of liver cancer.",
    "Is hepatitis B curable?": "While there is no specific cure for hepatitis B, antiviral medications can help manage the virus and reduce the risk of complications.",
    "Treatments for chronic hepatitis B?": "Several antiviral drugs are available to manage chronic hepatitis B, including entecavir, tenofovir, and others.",

    "Is there a cure for hepatitis B?": "While there is no specific cure for hepatitis B, antiviral medications can help manage the virus and reduce the risk of complications.",
    "What treatments (medicines) are available for chronic hepatitis B?": "Several antiviral drugs are available to manage chronic hepatitis B, including entecavir, tenofovir, and others.",
    "If the currently approved hepatitis B drugs do not provide a cure, then how are they helping?": "These drugs can suppress the virus, slow liver damage, and reduce the risk of complications.",
    "What can I do if I live in the U.S. and the insurance co-pay for my hepatitis B drugs costs too much for me to buy them?": "You can explore assistance programs or discuss more affordable treatment options with your healthcare provider.",
    "Is there any special diet for people living with chronic hepatitis B infection?": "A balanced and healthy diet is generally recommended. Consult your healthcare provider for personalized dietary advice.",
    "What blood tests are important to diagnose and evaluate my hepatitis B infection?": "Blood tests can measure hepatitis B surface antigen (HBsAg), hepatitis B e antigen (HBeAg), hepatitis B surface antibody (anti-HBs), and more to diagnose and monitor the infection.",
    "Does everyone with chronic hepatitis B need to take medicine?": "Not everyone needs medication. Treatment decisions depend on various factors, including the stage of the disease and the presence of liver damage.",
    "Will herbals, natural 'remedies', Ayurveda or Traditional Chinese Medicine, supplements, or vitamins and minerals control hepatitis B?": "These methods are not proven treatments for hepatitis B. Consult a healthcare provider for evidence-based treatment options.",
    "If I don't need to take medicine for my hepatitis B at this time, what must I do to support my liver?": "Maintain a healthy lifestyle, avoid excessive alcohol consumption, and follow your doctor's recommendations for monitoring your liver health.",
    "Can a hepatitis B infection be prevented? How can I protect my loved ones?": "Hepatitis B can be prevented through vaccination. Encourage your loved ones to get vaccinated.",
    "Is the hepatitis B vaccine safe?": "Yes, the hepatitis B vaccine is considered safe and effective.",
    "Is the hepatitis B vaccine safe during pregnancy?": "The vaccine is generally safe during pregnancy, and it may be recommended for women at risk of infection.",
    "Can I catch hepatitis B from the vaccine?": "No, the vaccine cannot cause a hepatitis B infection.",
    "Who is at risk of hepatitis B?": "One is at risk of hepatitis B if they are healthcare workers, recipients of blood products, intravenous drug users, multiple sexual activities, living in a family with someone with hepatitis B, among others.",
    "If I started the vaccine series but didn't complete my 2nd or 3rd dose on schedule, do I have to start over?": "Consult your healthcare provider, but in many cases, you can continue the series without starting over.",
    "I received my vaccine years ago--am I still protected?": "Vaccine protection may wane over time. Check with your doctor to determine if a booster is needed.",
    "Should I get the hepatitis B vaccine if I have a chronic HBV infection or have recovered from a past infection?": "Discuss with your healthcare provider, but in some cases, vaccination may still be recommended.",
    "Where can I get vaccinated against hepatitis B in the USA?": "You can get vaccinated at healthcare clinics, doctors' offices, or health departments. Contact your nearest health service centre for further guidance",
    "What should I do if I am diagnosed with chronic hepatitis B?": "Work closely with a healthcare provider to determine the best management plan for your specific case.",
    "I am diagnosed with chronic hepatitis B, can I get married and have children?": "Yes, but it's important to follow medical guidance to reduce the risk of transmission to your child.",
    "I am currently pregnant, and I have hepatitis B. What should I do to protect my baby?": "Administer the hepatitis B vaccine and hepatitis B immune globulin (HBIG) to your newborn to reduce the risk of transmission.",
    "Can I donate blood if I have hepatitis B?": "In most countries, individuals with hepatitis B are not allowed to donate blood.",
    "Diets or food for hepatitis B": "Whilst there are no specific foods for patients with hepatitis B, its generally recommended to eat a balanced diet, not avoiding meats; but a definite NO to alcohol and eating mouldy foods (risk of contamination by fungi)",
    "Prevention of hepatitis B infection": "The best way to prevent hepatitis B is by getting vaccinated. The hepatitis B vaccine is safe and effective. You need to get all shots in the series to be fully protected.",
    "If I have chronic hepatitis B infection, can I hug my children, partner or friend?": "Yes, casual contact, including hugging, is safe and does not transmit the virus.",
    "I’m in love, when and how do I tell my (prospective) partner that I have hepatitis B?": "Honesty is important. Discuss your hepatitis B status with your partner early in the relationship.",
    "If hepatitis B is sexually transmitted, how come my partner isn’t infected?": "Not all sexual partners will necessarily be infected. Use precautions and consider vaccination for your partner.",
    "If chronic hepatitis B is a silent disease, why do I have symptoms?": "Symptoms can occur, especially during acute flares or with more advanced liver disease.",
    "Sometimes I feel sad and depressed because of my hepatitis B status, what should I do?": "Consider seeking emotional support or counseling to help cope with the emotional impact of the condition.",
    "I keep hearing about a 'Functional Cure' for chronic hepatitis B, what does this mean?": "A functional cure means that the virus is suppressed to undetectable levels in the blood, even though it may still be present in liver tissue. It reduces the risk of liver disease and complications.",
    "What are the symptoms of hepatitis B?": "Common symptoms include jaundice, fatigue, abdominal pain, and dark urine.",
    "Is hepatitis B curable?": "There's no complete cure, but antiviral treatment can help manage the infection.",
    "Can hepatitis B be transmitted through saliva?": "Transmission through saliva is unlikely unless there are open sores or blood present.",
    "What is the prevalence of hepatitis B worldwide?": "An estimated 257 million people are living with hepatitis B globally.",
    "What is the Hepatitis B e antigen (HBeAg)?": "HBeAg is a marker of high viral replication in hepatitis B infection.",
    "How is hepatitis B diagnosed?": "Blood tests for hepatitis B surface antigen (HBsAg) and other markers are used for diagnosis.",
    "Are hepatitis B and hepatitis C the same?": "No, they are different viruses with distinct modes of transmission and treatments.",
    "Can I get a hepatitis B vaccine if I'm already infected?": "Yes, vaccination can prevent further infections.",
    "Is hepatitis B hereditary?": "No, it's not inherited genetically, but a mother can transmit it to her child during birth.",
    "Can hepatitis B cause liver cancer?": "Yes, chronic hepatitis B increases the risk of liver cancer.",
    "How is hepatitis B treated during pregnancy?": "Treatment is tailored to reduce the risk of transmission to the baby.",
    "Can hepatitis B be sexually transmitted to same-sex partners?": "Yes, it can be transmitted through sexual contact.",
    "Can hepatitis B be transmitted through food?": "Transmission through food is unlikely; it's primarily transmitted through blood and body fluids.",
    "What are the side effects of hepatitis B antiviral medications?": "Side effects can include fatigue, nausea, and diarrhea.",
    "What's the difference between acute and chronic hepatitis B?": "Acute is a short-term infection, while chronic persists for six months or more.",
    "How often should I get tested for hepatitis B?": "Testing frequency depends on risk factors and guidelines.",
    "What's the role of the liver in hepatitis B?": "The liver is the primary organ affected by hepatitis B.",
    "Can I drink alcohol with hepatitis B?": "Alcohol should be limited to protect the liver.",
    "Are there support groups for hepatitis B patients?": "Yes, support groups offer emotional and informational support.",
    "What are the long-term effects of chronic hepatitis B?": "It can lead to cirrhosis and an increased risk of liver cancer.",
    "Can hepatitis B be transmitted from mother to child during breastfeeding?": "Breastfeeding is safe when the infant receives the hepatitis B vaccine.",
    "Is there a hepatitis B cure in development?": "Ongoing research is exploring potential cures.",
    "Is hepatitis B a pandemic?": "It's a global health concern, but not classified as a pandemic.",
    "What precautions should healthcare workers take to prevent hepatitis B transmission?": "They should follow standard precautions and be vaccinated.",
    "How can I lower my risk of hepatitis B infection?": "Getting vaccinated is the most effective prevention method.",
    "Can I travel with hepatitis B?": "Yes, you can travel, but it's important to manage your health and carry necessary medications.",
    "What's the link between hepatitis B and hepatitis D?": "Hepatitis D can only infect those already infected with hepatitis B.",
    "What should I do if I'm exposed to hepatitis B?": "Seek medical advice and consider post-exposure prophylaxis (PEP).",
    "Can hepatitis B be transmitted through tattooing or piercing?": "Transmission can occur if equipment is not properly sterilized.",
    "Are there specific hepatitis B guidelines for healthcare providers?": "Healthcare providers should follow infection control practices and be vaccinated.",
    "What is the role of the liver in the human body?": "The liver performs many vital functions, including detoxification and metabolism.",
    "How can I access hepatitis B testing and treatment in low-resource areas?": "Organizations and clinics may offer testing and affordable treatment options.",
    "Are there hepatitis B vaccines for adults?": "Yes, adults can receive the hepatitis B vaccine.",
    "What organizations are involved in hepatitis B advocacy and research?": "Organizations like the WHO, Hepatitis B Foundation, and others work on hepatitis B issues.",
    "What is the relationship between hepatitis B and HIV?": "Coinfection with hepatitis B and HIV is possible and requires specialized care.",
    "Can hepatitis B be transmitted through mosquito bites?": "Transmission through mosquito bites is not a common route for hepatitis B.",
    "What is the hepatitis B core antibody (anti-HBc)?": "It's a marker of past or ongoing infection with hepatitis B.",
    "Can hepatitis B be transmitted through sharing food or utensils?": "Transmission through sharing food or utensils is unlikely.",
    "What's the cost of hepatitis B treatment in different countries?": "Treatment costs vary, and some countries offer affordable or free treatment.",
    "Is hepatitis B testing part of routine medical check-ups?": "It may not be included in routine check-ups, so request the test if needed.",
    "What are the hepatitis B risk factors for children?": "Children can be at risk if born to infected mothers or through exposure to infected household members.",
    "Can I use public swimming pools and hot tubs with hepatitis B?": "Yes, you can use public facilities; the virus doesn't spread through water.",
    "Is hepatitis B a notifiable disease?": "In many countries, healthcare providers are required to report hepatitis B cases to health authorities.",
    "What is the role of liver enzymes in hepatitis B diagnosis?": "Elevated liver enzymes can indicate liver damage due to hepatitis B.",
    "Can I participate in sports and physical activities with hepatitis B?": "Yes, you can participate in most activities, but consult your healthcare provider.",
    "Is hepatitis B lethal?": "Hepatitis B can be lethal, especially if it progresses to advanced liver disease or liver cancer. It's important to manage and monitor the infection.",
    "Is hepatitis B curable?": "Hepatitis B is not curable, but it can be managed with antiviral medications, reducing the risk of complications.",
    "Can I have children if hepatitis B positive?": "Yes, you can have children if you have hepatitis B. It's important to follow medical guidance to prevent transmission to your child, including administering the hepatitis B vaccine and hepatitis B immune globulin (HBIG) to your newborn.",
    "Will I die from hepatitis B?": "Not everyone with hepatitis B will die from the infection. Many people live with the virus without developing severe complications. Proper medical care and management can significantly improve outcomes.",
    "Can I eat, sleep, or use toilets with a hepatitis B patient and not get infected?": "Hepatitis B is primarily transmitted through blood and body fluids, not casual contact. You can share meals, sleep in the same room, and use the same toilets without the risk of transmission.",
    "What are the number of vaccination for hepatitis B?": "The number of doses required for the hepatitis B vaccine can depend on several factors, including the age of the individual, the type of vaccine being administered, and their specific health condition. However, for most healthy individuals, the standard hepatitis B vaccine schedule is a series of three doses.",
    "how many doses of hepatitis b vaccine is adequate?": "The number of doses required for the hepatitis B vaccine can depend on several factors, including the age of the individual, the type of vaccine being administered, and their specific health condition. However, for most healthy individuals, the standard hepatitis B vaccine schedule is a series of three doses.",
    "What is the chance of getting liver cancer if I have hepatitis B?": "Chronic hepatitis B significantly increases the risk of liver cancer. However, the risk varies depending on factors like your age, gender, and the presence of other liver diseases. Regular monitoring and medical care can help manage the risk.",
    "Treatment criteria for hepatitis B?": "Treatment for hepatitis B is typically recommended when specific criteria are met, including the presence of active liver inflammation, a high viral load, and evidence of liver fibrosis or cirrhosis. The decision to start treatment should be made by a healthcare provider based on your individual case and medical history. Regular monitoring of your liver health is crucial to determine the right time to initiate treatment.",
    "Hepatitis B vaccine schedule": "The standard vaccine schedule for both babies and adults receiving the hepatitis B vaccine typically consists of three doses. Here's the generic schedule: First Dose: The initial dose of the hepatitis B vaccine is often given at the first healthcare visit. Second Dose: The second dose is typically administered about 1 to 2 months after the first dose. Third Dose: The third and final dose is usually given approximately 6 months after the first dose. This dose completes the vaccination series.",
    "When does one qualify for treatment for hepatitis B?": "Treatment for hepatitis B is typically recommended when specific criteria are met, including the presence of active liver inflammation, a high viral load, and evidence of liver fibrosis or cirrhosis. The decision to start treatment should be made by a healthcare provider based on your individual case and medical history. Regular monitoring of your liver health is crucial to determine the right time to initiate treatment.",
    "Is hepatitis B transmissible via breastmilk?": "Yes, hepatitis B can be transmitted from mother to child through breast milk if the mother is a carrier of the virus. To prevent transmission, newborns are often given the hepatitis B vaccine and hepatitis B immune globulin (HBIG) at birth.",
    
    "What is the prognosis of hepatitis B?": "The prognosis of hepatitis B varies depending on factors like the age at which the infection was acquired and the presence of other liver diseases. Many people with hepatitis B can live healthy lives with medical management, while some may develop complications. Regular medical check-ups are essential to monitor liver health.",
    "Monitoring hepatitis B patients": "Monitoring a hepatitis B patient involves regular blood tests, including the hepatitis B Surface Antigen (HBsAg), Hepatitis B e Antigen (HBeAg), Hepatitis B Surface Antibody (anti-HBs), Hepatitis B Core Antibody (anti-HBc), and HBV DNA. Liver function tests, liver biopsy, and imaging may also be used. Regular check-ups and an Alpha-Fetoprotein (AFP) test for liver cancer are essential. The frequency of these tests varies by the patient's health and disease stage, determined in consultation with healthcare providers.",
    "Can one be totally cured from hepatitis B?": "While a complete cure for hepatitis B may not always be possible, antiviral medications can effectively control the virus, reduce liver inflammation, and prevent complications. Treatment can lead to undetectable levels of the virus in the blood, a state referred to as a 'functional cure.' It's important to consult a healthcare provider for personalized treatment options.",

    "Can I get hepatitis B from kissing?": "Hepatitis B can theoretically be transmitted through deep kissing if there is an exchange of blood, open sores, or other bodily fluids. However, the risk is relatively low compared to other forms of transmission, and practicing good oral hygiene and avoiding contact with infected blood can help reduce this risk.",

    "Can one get hepatitis B from saliva?": "The risk of contracting hepatitis B from saliva is extremely low, as the virus is not typically present in saliva. Transmission is more commonly associated with direct contact with infected blood, sexual activity, and sharing needles or personal items like razors.",

    "What is the most severe or serious complication of hepatitis B?": "The most serious complication of hepatitis B is the development of cirrhosis or liver cancer. Chronic hepatitis B can lead to liver damage and scarring (cirrhosis), which increases the risk of liver cancer (hepatocellular carcinoma). Regular monitoring and treatment can help prevent these severe complications.",

    "Does blood splashing to the eyes risk being infected by hepatitis B?": "The risk of hepatitis B transmission from blood splashing to the eyes is considered very low. However, it's important to take precautions to avoid direct contact with blood or other bodily fluids. If there is exposure to blood, you should wash your eyes thoroughly and seek medical advice if necessary.",

    "What is the first drug of choice for hepatitis B?": "The choice of the first-line drug for hepatitis B treatment may vary depending on factors such as the patient's age, medical history, and the presence of liver damage. Common antiviral drugs used to treat hepatitis B include tenofovir and entecavir. The selection of the most appropriate medication is determined by a healthcare provider.",

    "How long does it take from time of infection to manifestation of symptoms or incubation period of hepatitis B?": "The incubation period for hepatitis B can vary, but symptoms usually appear within one to six months after infection. Some individuals may remain asymptomatic, while others may develop symptoms sooner. It's essential to get tested and monitor your health regularly if you suspect hepatitis B exposure.",

}


# Function to find the best answer based on similarity score
def find_best_answer(user_input):
    user_input = user_input.lower()
    best_answer = None
    max_similarity = 0

    for question, answer in common_questions.items():
        similarity = fuzz.token_sort_ratio(user_input, question.lower())
        if similarity > max_similarity:
            best_answer = answer
            max_similarity = similarity

    return best_answer

# Function to find the best answer based on similarity score



st.markdown(
    f"<style>"
    f" .reportview-container .main .block-container{{"
    f" max-width: 1000px;"
    f" padding: 2rem 0;"
    f" }}"
    f"</style>",
    unsafe_allow_html=True
)


 
#st.title("Nimzing's Hepatitis B Chatbot 💬")
#st.header("Ask me anything about hepatitis B")

# Page title and header
st.markdown("<h1 style='text-align: center; color: #4472c4;'>Nimzing's Hepatitis B Chatbot 💬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Ask me anything about hepatitis B</p>", unsafe_allow_html=True)


# User input for the question
user_input = st.text_input("Ask a question (short single queries only and include hepatitis B in your question!):")

best_answer = None  # Initialize best_answer to None

if user_input:
    # Attempt to find the best answer based on similarity score
    best_answer = find_best_answer(user_input)

# Display the best answer if available
if best_answer:
    st.write("Best Answer:", best_answer)
else:
    st.write("I'm sorry, I don't have an answer to that question.")

# User feedback and question input
user_feedback = st.text_area("Provide feedback or ask more questions:")

if st.button("Send Feedback"):
    if user_feedback:
        # Send the feedback email
        def send_feedback_email():
            # Set up your email parameters
            sender_email = 'info@worthy-works.com'
            sender_password = 'kkoq dtwq nldp pcna'
            receiver_email = 'nimzing1@gmail.com'

            # Create an email message
            message = EmailMessage()
            message.set_content(user_feedback)
            message['Subject'] = 'User Feedback for Hepatitis B Chatbot'
            message['From'] = sender_email
            message['To'] = receiver_email

            # Connect to the SMTP server and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)

        send_feedback_email()
        st.markdown("<p style='color: #008000;'>Thank you for your feedback and questions. We appreciate your input.</p>", unsafe_allow_html=True)

        #st.write("Thank you for your feedback and questions. We appreciate your input.")
    else:
        #st.write("Please provide feedback or ask questions before sending.")
        st.markdown("<p style='color: #FF0000;'>Please provide feedback or ask questions before sending.</p>", unsafe_allow_html=True)


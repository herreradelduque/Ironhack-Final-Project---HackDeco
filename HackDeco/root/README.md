# Ironhack-Final-Project---HackDecó

![Alt text](./static/img/hackdeco.png?raw=true "Title")

# Description 🪑🔎   ➡️   💻 🤖 = 💺 

HackDecó enables the user to get a list of the most visualy similar pieces of furniture available at the main sellers websites, starting from a users image of a piece of furniture.

This project developes a CNN (Convolutional Neuronal Network), a web scrapping module, an API and a website. 

# Repo Structure 📂
/acquire: 
- Module: Web scrapping.
 
  
/analysis:
 
- Module: Features extraction (from sellers websites).

- Module: Features extraction (from an image of the user's piece furniture).

- Module: Visual recomendation.
 
 
/data:
- Images of furnitures
- Extracted features
- Visual recomendation (object)

requirements.txt:
- Required libraries.

app.py:
- API (Application Programming Interface).

README.md:
- Contains the main features needed to get a more comprehensive project.

webapp.py:
- HackDecó website

# Inputs🗃

- Images of furniture sellers websites: 

- User's image of a furniture.


# Usage ⛏

Users (at HackDecó website):
- selects the furniture seller website to analyze
- selects the type of furniture to search
- uploads an image of a furniture he/she wants to search, based on visual similarity
    
CNN model:
- converts the user's image into an numpy array
- applies a convolutional function
- extracts features at the last layer of the model

Cosine similarities:
- compares these features with all the features of the selected seller furniture

API:
- stablishes the chanel of communication between the endpoint and CNN model



# Stack ⚙

- Web scrapping: Selenium
- CNN (Convolutional Neural Networks): Keras
- API: Flask
- Data cleaning: Pandas and Numpy
- Data analiysis: SciKit-Learn
- Github

*For developer check 'requirements.txt'


# Output  📬

- The images of the more similar pieces of furniture rendered at Hackdecó website.

- Furniture's Price

- Buy url (seller's website)


-----------
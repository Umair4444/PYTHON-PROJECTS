1️⃣ Install Streamlit (If Not Installed)
If you haven't installed Streamlit, run:


bash
Copy
Edit
pip install streamlit

2️⃣ Navigate to Your Project Directory
Use the terminal or command prompt:

bash
Copy
Edit
cd path/to/your/project
For example:

bash
Copy
Edit
cd C:\Users\YourName\Project # Windows
cd ~/Project # macOS/Linux

3️⃣ Run the Streamlit App
Execute the following command:

bash
Copy
Edit
streamlit run app.py
🔹 This will start a local development server and display a URL like:

sql
Copy
Edit
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Click the link or open http://localhost:8501 in your browser.

4️⃣ Stop the Streamlit App
To stop the running app, press Ctrl + C in the terminal.

5️⃣ Running in a Virtual Environment (Optional)
If you are using a virtual environment (venv or conda), activate it before running Streamlit:

bash
Copy
Edit

# For virtualenv or venv

source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

# For Conda

conda activate myenv
Then run:

bash
Copy
Edit
streamlit run app.py
🔥 Pro Tips
✔ Use --server.port to specify a different port:

bash
Copy
Edit
streamlit run app.py --server.port 8080
✔ Deploy to Cloud using Streamlit Community Cloud: share.streamlit.io
✔ Auto-reload on save (enabled by default) → Just save app.py, and changes reflect instantly!

Would you like help deploying your Streamlit app? 🚀

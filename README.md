
# 📋 Sistema de Gestión de Secretaría Técnica

This is a **Streamlit-based web application** for managing and documenting public events such as **"Recorridos"** (walkthroughs) and **"Juntas Vecinales"** (neighborhood meetings). It includes user authentication, dynamic form inputs, map visualization, and **automatic PDF generation** using ReportLab.

## 🚀 Features

- 🔒 **Secure login system** 
- 🌍 **Interactive public map viewer** embedded via Google Maps
- 📝 **Detailed dynamic form** to register technical information about events
- 🧾 **Automatic PDF generation** for submitted event records
- 📷 Upload support for images (event croquis and photographic evidence)
- 🎨 Customized UI via injected HTML/CSS for better UX

## 🛠️ Technologies Used

- **Streamlit**: Web app framework for Python
- **ReportLab**: PDF generation
- **Google Maps Embed**: Public map visualization
- **HTML/CSS**: Custom styling and layout
- **Python libraries**: `datetime`, `io`, and `reportlab` submodules

## 📦 Installation

```bash
pip install streamlit reportlab
```

## ▶️ How to Run

1. Save the code in a file, e.g., `app.py`
2. Launch with Streamlit:

```bash
streamlit run app.py
```

## 🧑‍💼 Usage

1. **Login** using the access code: `igualdad2025`
2. **Navigate** via the sidebar to:
   - **Mapa Público** to view the embedded map
   - **Ficha Técnica** to fill and save event details
3. **Submit the form**, and a PDF is automatically generated summarizing the event.
4. Download or share the PDF as needed.

## 📄 Output

The generated PDF includes:
- Event metadata (type, duration, location)
- Responsible parties and section-level voting data
- Risk assessments and security plans
- Detailed descriptions for either a recorrido or a junta
- Visual evidence (if uploaded)

## 📬 Contact

For issues, contact the system admin or developer.

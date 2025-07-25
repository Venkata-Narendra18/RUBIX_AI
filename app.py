import streamlit as st
import openai
from PIL import Image
import base64
import io
import json

# Page configuration
st.set_page_config(
    page_title="RubixAI - Solve Your Rubik's Cube with AI",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced futuristic CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Global dark theme with cyberpunk colors */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Animated background particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(0, 255, 255, 0.3), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255, 0, 255, 0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 0, 0.3), transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(0, 255, 0, 0.3), transparent),
            radial-gradient(2px 2px at 160px 30px, rgba(255, 0, 0, 0.3), transparent);
        background-size: 200px 100px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes sparkle {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-100vh) rotate(360deg); }
    }
    
    /* Glowing main header */
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #00f5ff, #ff00ff, #ffff00, #ff0080);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        animation: gradient-shift 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
        letter-spacing: 3px;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        text-align: center;
        color: #00f5ff;
        font-size: 1.4rem;
        font-weight: 300;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.8);
        letter-spacing: 1px;
    }
    
    /* Glassmorphism effect for containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.4),
            0 0 25px rgba(0, 245, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    /* Enhanced face upload sections */
    .face-upload {
        background: rgba(0, 245, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 2px solid transparent;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .face-upload::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00f5ff, transparent, #ff00ff, transparent);
        border-radius: 15px;
        z-index: -1;
        animation: border-glow 2s linear infinite;
    }
    
    @keyframes border-glow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .face-upload:hover {
        transform: scale(1.02);
        background: rgba(0, 245, 255, 0.2);
    }
    
    .face-label {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        color: #00f5ff;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.8);
    }
    
    .face-complete {
        background: rgba(0, 255, 0, 0.15) !important;
        border-color: #00ff00 !important;
    }
    
    .face-complete::before {
        background: linear-gradient(45deg, #00ff00, transparent, #00ffff, transparent);
    }
    
    /* Futuristic solution box */
    .solution-box {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 245, 255, 0.5);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(0, 245, 255, 0.3);
    }
    
    .solution-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f5ff, transparent);
        animation: scan-line 3s linear infinite;
    }
    
    @keyframes scan-line {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(255, 0, 110, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(255, 0, 110, 0.6) !important;
        background: linear-gradient(45deg, #ff0080, #9d4edd, #4895ff) !important;
    }
    
    .stButton > button:disabled {
        background: rgba(100, 100, 100, 0.3) !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.8) !important;
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(0, 245, 255, 0.3) !important;
    }
    
    /* Toggle switch styling */
    .stCheckbox > label > div[data-testid="stCheckbox"] > div {
        background: linear-gradient(45deg, #ff006e, #8338ec) !important;
        border-radius: 20px !important;
    }
    
    /* File uploader enhancement */
    .stFileUploader {
        background: transparent !important;
    }
    
    .stFileUploader > div > div {
        background: rgba(0, 245, 255, 0.1) !important;
        border: 2px dashed rgba(0, 245, 255, 0.5) !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: rgba(0, 245, 255, 0.8) !important;
        background: rgba(0, 245, 255, 0.2) !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(90deg, rgba(0, 255, 0, 0.2), rgba(0, 255, 255, 0.2)) !important;
        border: 1px solid rgba(0, 255, 0, 0.5) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background: linear-gradient(90deg, rgba(255, 0, 0, 0.2), rgba(255, 0, 255, 0.2)) !important;
        border: 1px solid rgba(255, 0, 0, 0.5) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: linear-gradient(90deg, rgba(255, 255, 0, 0.2), rgba(255, 165, 0, 0.2)) !important;
        border: 1px solid rgba(255, 255, 0, 0.5) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Info box enhancement */
    .stInfo {
        background: linear-gradient(90deg, rgba(0, 245, 255, 0.2), rgba(138, 43, 226, 0.2)) !important;
        border: 1px solid rgba(0, 245, 255, 0.5) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Spinner enhancement */
    .stSpinner > div {
        border-top-color: #00f5ff !important;
        border-right-color: #ff00ff !important;
        border-bottom-color: #ffff00 !important;
        border-left-color: #ff0080 !important;
    }
    
    /* Column spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Image styling */
    .stImage {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stImage:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 12px 35px rgba(0, 245, 255, 0.4) !important;
    }
    
    /* Markdown enhancements */
    h1, h2, h3, h4, h5, h6 {
        color: #00f5ff !important;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 0 10px rgba(0, 245, 255, 0.5) !important;
    }
    
    /* Caption styling */
    .stImage > div > div > div {
        color: rgba(255, 255, 255, 0.8) !important;
        font-style: italic !important;
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #00f5ff, #0080ff) !important;
        box-shadow: 0 5px 15px rgba(0, 245, 255, 0.4) !important;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 25px rgba(0, 245, 255, 0.6) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #ff0080, #9d4edd, #4895ff);
    }
    
    /* Pulsing effect for important elements */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 245, 255, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 245, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 245, 255, 0); }
    }
    
    .pulse-effect {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

def initialize_openai():
    """Initialize OpenAI client with API key from Streamlit secrets"""
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return client
    except Exception as e:
        st.error(f"Failed to initialize OpenAI API: {str(e)}")
        st.error("Please make sure OPENAI_API_KEY is set in your Streamlit secrets.")
        return None

def encode_image(image):
    """Convert PIL image to base64 string for OpenAI API"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def analyze_cube_with_openai(client, face_images):
    """Send all 6 face images to OpenAI API and get solving instructions"""
    try:
        # Prepare images for API call
        image_contents = []
        face_names = ["Front", "Back", "Left", "Right", "Top", "Bottom"]
        
        for i, (face_name, image) in enumerate(zip(face_names, face_images)):
            if image is not None:
                base64_image = encode_image(image)
                image_contents.append({
                    "type": "text",
                    "text": f"**{face_name} Face:**"
                })
                image_contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high"
                    }
                })
        
        # Create comprehensive prompt for all 6 faces
        prompt = """
        You are an expert Rubik's Cube solver. I'm providing you with images of all 6 faces of a Rubik's Cube in this order:
        1. Front Face
        2. Back Face  
        3. Left Face
        4. Right Face
        5. Top Face
        6. Bottom Face
        
        Please analyze each face carefully and:
        
        1. **Identify the colors** on each face and their positions (use a 3x3 grid notation)
        2. **Determine the current cube state** by mapping all visible stickers
        3. **Generate a complete step-by-step solution** using the Layer-by-Layer (beginner's) method
        4. **Provide specific moves** using standard notation (R, L, U, D, F, B, with ', 2 modifiers)
        5. **Organize by phases**: White Cross → White Corners → Middle Layer → Yellow Cross → Yellow Face → Final Layer
        
        **Important Guidelines:**
        - Assume standard cube colors: White opposite Yellow, Red opposite Orange, Blue opposite Green
        - Provide the exact sequence of moves needed
        - Explain what each phase accomplishes
        - Include tips for executing moves correctly
        - If any face image is unclear, mention it but provide the best possible solution
        
        **Response Format:**
        
        **CUBE STATE ANALYSIS:**
        [Brief description of current state]
        
        **PHASE 1: WHITE CROSS**
        Goal: Form a white cross on the bottom face with matching edge colors
        1. [Specific moves] - [Explanation]
        2. [Specific moves] - [Explanation]
        
        **PHASE 2: WHITE CORNERS**
        Goal: Complete the white face (bottom layer)
        [Continue with numbered steps...]
        
        **PHASE 3: MIDDLE LAYER**
        Goal: Position the middle layer edge pieces
        [Continue with numbered steps...]
        
        **PHASE 4: YELLOW CROSS**
        Goal: Form a yellow cross on the top face
        [Continue with numbered steps...]
        
        **PHASE 5: YELLOW FACE**
        Goal: Complete the yellow face
        [Continue with numbered steps...]
        
        **PHASE 6: FINAL LAYER**
        Goal: Position and orient the final layer
        [Continue with numbered steps...]
        
        Please be as specific and detailed as possible with the move sequences.
        """
        
        # Combine prompt with images
        message_content = [{"type": "text", "text": prompt}] + image_contents
        
        # Make API call to OpenAI using the correct current syntax
        response = client.chat.completions.create(
            model="gpt-4o",  # Using gpt-4o as requested
            messages=[{
                "role": "user",
                "content": message_content
            }],
            max_tokens=3000,
            temperature=0.2
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error analyzing cube: {str(e)}"

def main():
    # Initialize session state for face images
    if 'face_images' not in st.session_state:
        st.session_state.face_images = [None] * 6
    
    # Sidebar with app information
    with st.sidebar:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("### 🧩 About RubixAI")
        st.markdown("""
        RubixAI analyzes all 6 faces of your Rubik's Cube to provide 
        accurate step-by-step solving instructions.
        
        **How to use:**
        1. Take clear photos of all 6 cube faces
        2. Upload each face in the correct order
        3. Click 'Generate Complete Solution'
        4. Follow the detailed phase-by-phase instructions
        
        **Photo Tips:**
        - Good lighting is essential
        - Hold cube steady and flat
        - Ensure all 9 stickers are clearly visible
        - Avoid shadows and glare
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown("### 🎨 Cube Notation")
        st.markdown("""
        **Basic Moves:**
        - **R** = Right face clockwise
        - **L** = Left face clockwise  
        - **U** = Up face clockwise
        - **D** = Down face clockwise
        - **F** = Front face clockwise
        - **B** = Back face clockwise
        
        **Modifiers:**
        - **'** = Counter-clockwise (R')
        - **2** = Double turn (R2)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upload progress indicator
        uploaded_count = sum(1 for img in st.session_state.face_images if img is not None)
        st.markdown('<div class="glass-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown("### 📊 Upload Progress")
        progress = uploaded_count / 6
        st.progress(progress)
        st.write(f"**{uploaded_count}/6** faces uploaded")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Theme toggle
        st.markdown('<div class="glass-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
        st.markdown("### 🎨 Advanced Mode")
        dark_mode = st.toggle("🌌 Quantum Enhancement", value=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Main header
    st.markdown('<h1 class="main-header">🧩 RubixAI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Complete 6-Face Rubik\'s Cube Solver</p>', unsafe_allow_html=True)
    
    # Initialize OpenAI
    client = initialize_openai()
    if client is None:
        st.stop()
    
    # Instructions
    st.markdown("### 📸 Upload All 6 Cube Faces")
    st.info("🔥 **Important:** For accurate solving, please upload clear images of all 6 faces of your cube. Each face should show all 9 colored stickers clearly.")
    
    # Create layout for face uploads
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        # Face upload section
        face_names = ["Front", "Back", "Left", "Right", "Top", "Bottom"]
        face_descriptions = [
            "The face you're looking at directly",
            "The face opposite to the front",
            "The face to your left when looking at front",
            "The face to your right when looking at front", 
            "The face on top of the cube",
            "The face on the bottom of the cube"
        ]
        
        # Create grid layout for face uploads
        for i in range(0, 6, 2):
            subcol1, subcol2 = st.columns(2)
            
            for j, subcol in enumerate([subcol1, subcol2]):
                face_idx = i + j
                if face_idx < 6:
                    with subcol:
                        face_name = face_names[face_idx]
                        face_desc = face_descriptions[face_idx]
                        
                        # Add styling based on upload status
                        css_class = "face-upload face-complete" if st.session_state.face_images[face_idx] is not None else "face-upload"
                        
                        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                        st.markdown(f'<div class="face-label">📱 {face_name} Face</div>', unsafe_allow_html=True)
                        st.caption(face_desc)
                        
                        uploaded_file = st.file_uploader(
                            f"Upload {face_name} face",
                            type=["png", "jpg", "jpeg"],
                            key=f"face_{face_idx}",
                            label_visibility="collapsed"
                        )
                        
                        if uploaded_file is not None:
                            image = Image.open(uploaded_file)
                            st.session_state.face_images[face_idx] = image
                            st.image(image, caption=f"{face_name} Face", width=150)
                        elif st.session_state.face_images[face_idx] is not None:
                            st.image(st.session_state.face_images[face_idx], caption=f"{face_name} Face", width=150)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("### 📋 Upload Checklist")
        
        # Display checklist of uploaded faces
        for i, face_name in enumerate(face_names):
            if st.session_state.face_images[i] is not None:
                st.success(f"✅ {face_name} Face")
            else:
                st.error(f"❌ {face_name} Face")
        
        # Generate solution button
        all_faces_uploaded = all(img is not None for img in st.session_state.face_images)
        
        if all_faces_uploaded:
            st.success("🎉 All faces uploaded! Ready to solve.")
            
            if st.button("🚀 Generate Complete Solution", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing all 6 faces of your cube..."):
                    solution = analyze_cube_with_openai(client, st.session_state.face_images)
                
                # Store solution in session state
                st.session_state.solution = solution
                st.session_state.cube_analyzed = True
        else:
            remaining = 6 - sum(1 for img in st.session_state.face_images if img is not None)
            st.warning(f"⏳ Please upload {remaining} more face(s)")
            st.button("🚀 Generate Complete Solution", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display solution
    if hasattr(st.session_state, 'solution') and st.session_state.cube_analyzed:
        st.markdown("---")
        st.markdown("## 🎯 Complete Solving Solution")
        
        st.markdown('<div class="solution-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.solution)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Clear All & Start Over", use_container_width=True):
                st.session_state.face_images = [None] * 6
                if hasattr(st.session_state, 'solution'):
                    del st.session_state.solution
                if hasattr(st.session_state, 'cube_analyzed'):
                    del st.session_state.cube_analyzed
                st.rerun()
        
        with col2:
            st.download_button(
                label="💾 Download Solution",
                data=st.session_state.solution,
                file_name="rubiks_cube_complete_solution.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Re-analyze Cube", use_container_width=True):
                with st.spinner("🤖 Re-analyzing your cube..."):
                    solution = analyze_cube_with_openai(client, st.session_state.face_images)
                st.session_state.solution = solution
                st.rerun()
        
        # Additional tips
        st.markdown('<div class="glass-container" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown("### 💡 Solving Tips")
        st.info("""
        **General Tips:**
        - Work through each phase completely before moving to the next
        - Take your time and double-check each move
        - If you make a mistake, don't panic! Continue from your current position
        - Practice the notation until moves become second nature
        - Keep the solved white face on the bottom throughout phases 3-6
        
        **If Solution Seems Wrong:**
        - Ensure all face photos were clear and well-lit
        - Double-check that you uploaded the correct face for each position
        - Try re-taking photos with better lighting/angles
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; margin-top: 3rem;'>
        <div class="glass-container" style="display: inline-block; padding: 2rem;">
            <h3 style='color: #00f5ff; font-family: "Orbitron", monospace; margin-bottom: 1rem;'>
                🧩 RubixAI - Quantum Cube Analysis
            </h3>
            <p style='color: rgba(255, 255, 255, 0.8); font-size: 1.1rem; margin-bottom: 0.5rem;'>
                Powered by OpenAI GPT-4 Vision & Advanced AI Algorithms
            </p>
            <p style='color: #ff00ff; font-style: italic; font-size: 0.9rem;'>
                Upload all 6 faces for the most accurate solving solution!
            </p>
            <div style='margin-top: 1rem;'>
                <span style='color: #00f5ff; font-size: 0.8rem; opacity: 0.7;'>
                    ⚡ Enhanced with Cyberpunk UI • 🌌 Quantum Processing • 🔮 Future-Ready
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from io import BytesIO
from PIL import Image
import qrcode.image.svg

# Page configuration
st.set_page_config(
    page_title="AI QR Generator Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stDownloadButton button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="feature-card">
        <h1 style="margin:0;">🚀 Professional QR Code Generator</h1>
        <p style="margin:0.5rem 0 0 0; opacity:0.9;">Create stunning, customizable QR codes with advanced features</p>
    </div>
""", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📝 QR Code Content")
    
    # Content type selection
    content_type = st.selectbox(
        "Content Type",
        ["URL", "Text", "Email", "Phone", "SMS", "WiFi"],
        help="Select the type of content you want to encode"
    )
    
    # Dynamic input based on content type
    if content_type == "URL":
        url = st.text_input(
            "Enter URL:",
            placeholder="https://example.com",
            help="Enter the full URL including http:// or https://"
        )
        qr_data = url
        
    elif content_type == "Text":
        text = st.text_area(
            "Enter Text:",
            placeholder="Your text here...",
            height=100
        )
        qr_data = text
        
    elif content_type == "Email":
        email = st.text_input("Email Address:", placeholder="example@email.com")
        subject = st.text_input("Subject (optional):", placeholder="Email subject")
        body = st.text_area("Message (optional):", placeholder="Email body", height=100)
        qr_data = f"mailto:{email}?subject={subject}&body={body}" if email else ""
        
    elif content_type == "Phone":
        phone = st.text_input("Phone Number:", placeholder="+1234567890")
        qr_data = f"tel:{phone}" if phone else ""
        
    elif content_type == "SMS":
        phone = st.text_input("Phone Number:", placeholder="+1234567890")
        message = st.text_area("Message:", placeholder="Your message", height=100)
        qr_data = f"sms:{phone}?body={message}" if phone else ""
        
    elif content_type == "WiFi":
        ssid = st.text_input("Network Name (SSID):", placeholder="MyWiFi")
        password = st.text_input("Password:", type="password", placeholder="WiFi password")
        security = st.selectbox("Security Type:", ["WPA", "WEP", "nopass"])
        hidden = st.checkbox("Hidden Network")
        if ssid:
            qr_data = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
        else:
            qr_data = ""

# Sidebar customization
with st.sidebar:
    st.header("⚙️ Customization Settings")
    
    st.subheader("🎨 Colors")
    fill_color = st.color_picker("QR Code Color", "#000000")
    back_color = st.color_picker("Background Color", "#FFFFFF")
    
    st.subheader("🔧 Advanced Settings")
    
    # Error correction level
    error_correction = st.selectbox(
        "Error Correction Level",
        ["Low (7%)", "Medium (15%)", "Quartile (25%)", "High (30%)"],
        index=1,
        help="Higher levels allow the QR code to be read even if partially damaged"
    )
    
    error_correction_map = {
        "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
        "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
        "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
        "High (30%)": qrcode.constants.ERROR_CORRECT_H
    }
    
    # QR Code style
    qr_style = st.selectbox(
        "QR Code Style",
        ["Square", "Rounded", "Circles", "Gapped Squares"],
        help="Choose the visual style of the QR code modules"
    )
    
    # Size settings
    box_size = st.slider("Module Size", 5, 20, 10, help="Size of each QR code box")
    border = st.slider("Border Size", 1, 10, 4, help="Width of the border around the QR code")
    
    st.subheader("📏 Output Settings")
    output_size = st.slider("Output Image Size (px)", 200, 1000, 400, step=50)
    
    st.divider()
    
    # Info section
    with st.expander("ℹ️ About QR Codes"):
        st.write("""
        **Error Correction Levels:**
        - **Low**: Can recover 7% of data
        - **Medium**: Can recover 15% of data
        - **Quartile**: Can recover 25% of data
        - **High**: Can recover 30% of data
        
        Higher error correction allows QR codes to be read even when partially damaged or obscured.
        """)

# Generate QR Code
with col2:
    st.subheader("🎯 Generated QR Code")
    
    if qr_data:
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_correction_map[error_correction],
                box_size=box_size,
                border=border,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Apply style
            style_map = {
                "Square": None,
                "Rounded": RoundedModuleDrawer(),
                "Circles": CircleModuleDrawer(),
                "Gapped Squares": GappedSquareModuleDrawer()
            }
            
            module_drawer = style_map[qr_style]
            
            if module_drawer:
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=module_drawer,
                    color_mask=SolidFillColorMask(
                        back_color=back_color,
                        front_color=fill_color
                    )
                )
            else:
                img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Resize image
            img = img.resize((output_size, output_size), Image.Resampling.LANCZOS)
            
            # Display QR code
            buf = BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.image(byte_im, use_container_width=True)
            
            # Success message
            st.markdown("""
                <div class="success-box">
                    ✅ QR Code generated successfully!
                </div>
            """, unsafe_allow_html=True)
            
            # Download section
            st.subheader("📥 Download Options")
            
            col_png, col_svg = st.columns(2)
            
            with col_png:
                st.download_button(
                    label="Download PNG",
                    data=byte_im,
                    file_name=f"qrcode_{content_type.lower()}.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            with col_svg:
                # Generate SVG version
                svg_buf = BytesIO()
                svg_qr = qrcode.QRCode(
                    version=1,
                    error_correction=error_correction_map[error_correction],
                    box_size=box_size,
                    border=border,
                )
                svg_qr.add_data(qr_data)
                svg_qr.make(fit=True)
                
                # Create SVG
                factory = qrcode.image.svg.SvgPathImage
                svg_img = svg_qr.make_image(image_factory=factory, fill_color=fill_color, back_color=back_color)
                svg_img.save(svg_buf)
                svg_data = svg_buf.getvalue()
                
                st.download_button(
                    label="Download SVG",
                    data=svg_data,
                    file_name=f"qrcode_{content_type.lower()}.svg",
                    mime="image/svg+xml",
                    use_container_width=True
                )
            
            # QR Code info
            with st.expander("📊 QR Code Information"):
                st.write(f"**Content Type:** {content_type}")
                st.write(f"**Error Correction:** {error_correction}")
                st.write(f"**Style:** {qr_style}")
                st.write(f"**Size:** {output_size}x{output_size} pixels")
                st.write(f"**Data Length:** {len(qr_data)} characters")
                
        except Exception as e:
            st.error(f"❌ Error generating QR code: {str(e)}")
            st.info("Please check your input and try again.")
    else:
        st.info("👈 Enter content in the form to generate your QR code")
        
        # Show example QR code
        st.markdown("### Example QR Code")
        example_qr = qrcode.QRCode(version=1, box_size=10, border=4)
        example_qr.add_data("https://github.com")
        example_qr.make(fit=True)
        example_img = example_qr.make_image(fill_color="#667eea", back_color="#ffffff")
        example_img = example_img.resize((300, 300), Image.Resampling.LANCZOS)
        
        example_buf = BytesIO()
        example_img.save(example_buf, format="PNG")
        st.image(example_buf.getvalue(), caption="Example: GitHub QR Code", width=300)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; opacity: 0.7; padding: 1rem;">
        <p>💡 Tip: Higher error correction levels create more complex QR codes that work better with logos or when partially covered.</p>
        <p>Made with ❤️ using Streamlit • QR Code Generator Pro v2.0</p>
    </div>
""", unsafe_allow_html=True)
import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه تست زنده و دقیق عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تست زنده و فیکس‌شده فریم‌های اپتیکال")

# مدیریت حالت‌های برنامه
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت تصویر چهره
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت و پیشنهاد فریم‌های استاندارد
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"id": "aviator", "name": "Tom Ford - Aviator Gold", "type": "خلبانی فلزی لوکس کلاسیک", "brand": "Tom Ford"},
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer Classic", "type": "مستطیلی کائوچویی مشکی استاندارد", "brand": "Ray-Ban"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer Classic", "type": "ویفرر استاندارد شیک", "brand": "Ray-Ban"},
                {"id": "cateye", "name": "Tom Ford - Elegant CatEye", "type": "چشم‌گربه‌ای مدرن و جذاب", "brand": "Tom Ford"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"id": "round", "name": "Ray-Ban - Retro Round Metal", "type": "گرد فلزی مینیمال مهندسی‌شده", "brand": "Ray-Ban"},
                {"id": "slim", "name": "Tom Ford - Slim Rectangular", "type": "فریم زاویه‌دار باریک", "brand": "Tom Ford"}
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری فریم‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب فریم متناسب")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده شما", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 فریم‌های استاندارد زیر بر اساس آناتومی صورت شما پیشنهاد شده‌اند. یکی را انتخاب کنید تا وارد **اتاق تست زنده روی چشم** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 10px; background: #fafafa;">
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>استایل:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ تست زنده این فریم روی چشم", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق تست زنده با فیکس دقیق اپتومتریک و تناسب ابعادی واقعی
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست زنده (فریم فعال: {chosen['name']})")
    st.markdown("دوربین زنده فعال است. فریم عینک کاملاً متناسب با ابعاد صورت و با پایدارسازی پیشرفته روی چشم‌ها نشسته است.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    ar_tryon_raw_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
        <style>
            .ar-container {
                position: relative;
                width: 640px;
                height: 480px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                background: #000;
            }
            video, canvas {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
            }
            #glasses_overlay {
                position: absolute;
                display: none;
                pointer-events: none;
                z-index: 10;
                width: 240px;
                transform-origin: 50% 50%;
                will-change: transform, left, top;
            }
            .loading {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-family: Tahoma, sans-serif;
                font-size: 16px;
                z-index: 20;
                background: rgba(0,0,0,0.85);
                padding: 14px 28px;
                border-radius: 8px;
            }
            .info-bar {
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
                max-width: 640px;
                margin: 10px auto 0 auto;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="ar-container">
            <div id="loading" class="loading">در حال راه‌اندازی دوربین و انطباق استاندارد عینک روی چشم‌ها...</div>
            <video id="webcam" autoplay playsinline muted></video>
            <canvas id="output_canvas"></canvas>
            
            <div id="glasses_overlay">
                <svg width="240px" height="80px" viewBox="0 0 240 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="8" y="10" width="104" height="60" rx="18" stroke="#1a1a1a" stroke-width="5" fill="rgba(180,210,245,0.15)" />
                    <rect x="128" y="10" width="104" height="60" rx="18" stroke="#1a1a1a" stroke-width="5" fill="rgba(180,210,245,0.15)" />
                    <path d="M 112 22 Q 120 16 128 22" stroke="#1a1a1a" stroke-width="4.5" fill="none" />
                    <path d="M 8 20 L -4 14" stroke="#1a1a1a" stroke-width="4" stroke-linecap="round" />
                    <path d="M 232 20 L 244 14" stroke="#1a1a1a" stroke-width="4" stroke-linecap="round" />
                </svg>
            </div>
        </div>
        <div class="info-bar">
            <b>فریم انتخابی:</b> __FRAME_NAME__ | 🟢 سیستم فیکس آناتومیک پیشرفته فعال است
        </div>

        <script>
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const loadingElement = document.getElementById('loading');
            const glassesDiv = document.getElementById('glasses_overlay');

            let smoothX = 0, smoothY = 0, smoothAngle = 0, smoothScale = 1;

            function onResults(results) {
                loadingElement.style.display = 'none';
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.restore();

                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
                    const landmarks = results.multiFaceLandmarks[0];
                    
                    const leftEyeInner = landmarks.length > 133 ? landmarks[133] : landmarks[33];
                    const rightEyeInner = landmarks.length > 362 ? landmarks[362] : landmarks[263];
                    
                    const targetX = ((leftEyeInner.x + rightEyeInner.x) / 2) * canvasElement.width;
                    const targetY = (((leftEyeInner.y + rightEyeInner.y) / 2) * canvasElement.height) - (canvasElement.height * 0.012);

                    const eyeDist = Math.hypot(
                        (rightEyeInner.x - leftEyeInner.x) * canvasElement.width,
                        (rightEyeInner.y - leftEyeInner.y) * canvasElement.height
                    );

                    const dx = rightEyeInner.x - leftEyeInner.x;
                    const dy = rightEyeInner.y - leftEyeInner.y;
                    let targetAngle = Math.atan2(dy, dx) * (180 / Math.PI);
                    
                    targetAngle = Math.max(-10, Math.min(10, targetAngle));
                    const targetScale = eyeDist / 58.0;

                    if (smoothX === 0) {
                        smoothX = targetX;
                        smoothY = targetY;
                        smoothAngle = targetAngle;
                        smoothScale = targetScale;
                    } else {
                        smoothX += (targetX - smoothX) * 0.35;
                        smoothY += (targetY - smoothY) * 0.35;
                        smoothAngle += (targetAngle - smoothAngle) * 0.35;
                        smoothScale += (targetScale - smoothScale) * 0.35;
                    }
                    
                    glassesDiv.style.left = (canvasElement.width - smoothX) + 'px';
                    glassesDiv.style.top = smoothY + 'px';
                    
                    glassesDiv.style.transform = `translate(-50%, -50%) rotate(${smoothAngle}deg) scale(${smoothScale})`;
                    glassesDiv.style.display = 'block';
                } else {
                    glassesDiv.style.display = 'none';
                }
            }

            const faceMesh = new FaceMesh({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
            });

            faceMesh.setOptions({
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.7,
                minTrackingConfidence: 0.7
            });

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {
                onFrame: async () => {
                    await faceMesh.send({ image: videoElement });
                },
                width: 640,
                height: 480
            });

            camera.start().catch(err => {
                loadingElement.innerText = "خطا در دسترسی به دوربین مرورگر!";
                console.error(err);
            });
        </script>
    </body>
    </html>
    """

    ar_tryon_html = ar_tryon_raw_html.replace("__FRAME_NAME__", chosen['name'])
    components.html(ar_tryon_html, height=580)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()
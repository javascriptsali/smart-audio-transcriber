"""
Streamlit UI for Smart Audio Transcriber.
Bilingual support (English/Persian) with toggle.
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import os

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.transcriber import get_transcriber

# ==========================================
# Translations Dictionary
# ==========================================
TRANSLATIONS = {
    'en': {
        'title': '🎙️ Smart Audio Transcriber',
        'subtitle': 'Convert audio to text with AI (Full support for Persian and English)',
        'settings': '⚙️ Model Settings',
        'model_select': 'Select Whisper Model',
        'language_select': 'Audio Language',
        'language_auto': 'Auto-detect',
        'language_fa': 'Persian',
        'language_en': 'English',
        'vad_toggle': '🎯 Filter non-speech sounds (VAD)',
        'vad_help': "Enable for pure audio (podcasts). Disable for songs or background music.",
        'upload': '📁 Upload your audio or video file',
        'upload_help': "Supported formats: MP3, WAV, M4A, FLAC, MP4, OGG",
        'transcribe_btn': '🎤 Start Transcription',
        'processing': '⏳ Loading model and processing... (this may take a moment)',
        'success': '✅ Processing completed successfully!',
        'no_speech': '⚠️ **No human speech detected in this file.**\n\nThis may be because:\n- File contains only music or ambient sound\n- Audio quality is very low\n- File language doesn\'t match selected language',
        'detected_lang': '🌐 Detected Language',
        'lang_confidence': '🎯 Language Confidence',
        'duration': '⏱️ Duration',
        'seconds': 'seconds',
        'full_text': '📝 Full Text:',
        'timestamps': '⏱️ Timestamps Table:',
        'col_start': 'Start (s)',
        'col_end': 'End (s)',
        'col_text': 'Text',
        'download_btn': '📥 Download Text (TXT)',
        'error': '❌ Processing error:',
        'upload_prompt': '👆 Please upload an audio or video file to start processing.',
        'use_cases': '### 💡 Use Cases:',
        'use_case_1': '🎙️ **Auto-transcribe meetings and interviews**',
        'use_case_2': '🎬 **Auto-generate video subtitles**',
        'use_case_3': '🇮🇷 **Excellent Persian language support**',
        'guide_title': '**💡 Guide:**',
        'guide_1': '- For good quality Persian files, **Base** or **Small** models work well.',
        'guide_2': '- If auto-detect chooses wrong language, lock it to "Persian".',
        'guide_3': '- Processing is **completely local** - your file is never uploaded.',
        'lang_toggle': '🌐 زبان / Language'
    },
    'fa': {
        'title': '🎙️ تبدیل هوشمند صدا به متن',
        'subtitle': 'تبدیل صدا به متن با هوش مصنوعی (پشتیبانی کامل از فارسی و انگلیسی)',
        'settings': '⚙️ تنظیمات مدل',
        'model_select': 'انتخاب مدل Whisper',
        'language_select': 'زبان صدا',
        'language_auto': 'تشخیص خودکار',
        'language_fa': 'فارسی',
        'language_en': 'انگلیسی',
        'vad_toggle': '🎯 فیلتر کردن صداهای غیرگفتاری (VAD)',
        'vad_help': "برای فایل‌های صوتی خالص (مثل پادکست) فعال بگذارید. برای آهنگ‌ها یا فایل‌های با موسیقی پس‌زمینه، غیرفعال کنید.",
        'upload': '📁 فایل صوتی یا ویدیویی خود را آپلود کنید',
        'upload_help': "فرمت‌های پشتیبانی‌شده: MP3, WAV, M4A, FLAC, MP4, OGG",
        'transcribe_btn': '🎤 شروع تبدیل صدا به متن',
        'processing': '⏳ در حال بارگذاری مدل و پردازش... (این کار ممکن است چند لحظه طول بکشد)',
        'success': '✅ پردازش فایل با موفقیت انجام شد!',
        'no_speech': '⚠️ **هیچ گفتار انسانی در این فایل تشخیص داده نشد.**\n\nاین ممکن است به دلیل موارد زیر باشد:\n- فایل فقط حاوی موسیقی یا صدای محیط است\n- کیفیت صدا بسیار پایین است\n- زبان فایل با زبان انتخاب‌شده مطابقت ندارد',
        'detected_lang': '🌐 زبان تشخیص‌داده‌شده',
        'lang_confidence': '🎯 اطمینان از زبان',
        'duration': '⏱️ مدت زمان',
        'seconds': 'ثانیه',
        'full_text': '📝 متن کامل:',
        'timestamps': '⏱️ جدول زمان‌بندی:',
        'col_start': 'شروع (ثانیه)',
        'col_end': 'پایان (ثانیه)',
        'col_text': 'متن',
        'download_btn': '📥 دانلود متن (TXT)',
        'error': '❌ خطا در پردازش:',
        'upload_prompt': '👆 لطفاً یک فایل صوتی یا ویدیویی آپلود کنید تا پردازش شروع شود.',
        'use_cases': '### 💡 موارد استفاده:',
        'use_case_1': '🎙️ **تایپ خودکار جلسات و مصاحبه‌ها**',
        'use_case_2': '🎬 **زیرنویس‌سازی خودکار ویدیوها**',
        'use_case_3': '🇮🇷 **پشتیبانی عالی از زبان فارسی**',
        'guide_title': '**💡 راهنما:**',
        'guide_1': '- برای فایل‌های فارسی با کیفیت خوب، مدل **Base** یا **Small** عالی هستند.',
        'guide_2': '- اگر مدل روی "تشخیص خودکار" است و زبان را اشتباه تشخیص داد، آن را روی "فارسی" قفل کنید.',
        'guide_3': '- پردازش به صورت **کاملاً لوکال** انجام می‌شود و فایل شما آپلود نمی‌شود.',
        'lang_toggle': '🌐 Language / زبان'
    }
}

def t(key):
    """Helper function to get translation."""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS[lang].get(key, key)

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Smart Audio Transcriber",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Initialize Session State
# ==========================================
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# ==========================================
# Custom CSS
# ==========================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Header
# ==========================================
st.markdown(f'<div class="main-header">{t("title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{t("subtitle")}</div>', unsafe_allow_html=True)

# ==========================================
# Sidebar Settings
# ==========================================
with st.sidebar:
        # Language Toggle with instant update
    def on_language_change():
        """Update language immediately when selection changes."""
        choice = st.session_state.lang_select_key
        st.session_state.language = 'en' if choice == 'English' else 'fa'
    
    st.selectbox(
        '🌐 Language / زبان',
        options=['English', 'فارسی'],
        index=0 if st.session_state.language == 'en' else 1,
        key='lang_select_key',
        on_change=on_language_change
    )
    
    st.divider()
    
    st.header(t('settings'))
    
    model_options = {
        'Tiny (39 MB) - Fastest': 'tiny',
        'Base (74 MB) - Recommended': 'base',
        'Small (244 MB) - More accurate': 'small',
        'Medium (769 MB) - Professional': 'medium',
        'Large-v3 (1.5 GB) - Best accuracy': 'large-v3'
    }
    
    selected_model_name = st.selectbox(
        t('model_select'),
        options=list(model_options.keys()),
        index=1
    )
    model_key = model_options[selected_model_name]
    
    st.divider()
    
    language_options = {
        t('language_auto'): None,
        t('language_fa'): 'fa',
        t('language_en'): 'en'
    }
    selected_lang_name = st.selectbox(
        t('language_select'),
        options=list(language_options.keys()),
        index=0
    )
    lang_code = language_options[selected_lang_name]
    
    st.divider()
    
    enable_vad = st.checkbox(
        t('vad_toggle'),
        value=True,
        help=t('vad_help')
    )
    
    st.divider()
    
    st.info(f"{t('guide_title')}\n{t('guide_1')}\n{t('guide_2')}\n{t('guide_3')}")

# ==========================================
# Main Content
# ==========================================
uploaded_file = st.file_uploader(
    t('upload'),
    type=['mp3', 'wav', 'm4a', 'flac', 'mp4', 'ogg'],
    help=t('upload_help')
)

if uploaded_file is not None:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[-1]}")
    
    temp_dir = "data/temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.divider()
    
    if st.button(t('transcribe_btn'), type="primary", use_container_width=True):
        with st.spinner(t('processing')):
            try:
                transcriber = get_transcriber(model_name=model_key)
                result = transcriber.transcribe(
                    temp_file_path, 
                    language=lang_code,
                    enable_vad=enable_vad
                )
                
                if not result['segments']:
                    st.warning(t('no_speech'))
                else:
                    st.success(t('success'))
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric(t('detected_lang'), result['detected_language'].upper())
                    col2.metric(t('lang_confidence'), f"{result['language_probability'] * 100:.1f}%")
                    col3.metric(t('duration'), f"{result['duration_seconds']} {t('seconds')}")
                    
                    st.divider()
                    
                    st.subheader(t('full_text'))
                    st.markdown(f"<div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; line-height: 1.8;'>{result['text']}</div>", unsafe_allow_html=True)
                    
                    st.divider()
                    
                    st.subheader(t('timestamps'))
                    df = pd.DataFrame(result['segments'])
                    df.columns = [t('col_start'), t('col_end'), t('col_text')]
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.download_button(
                        label=t('download_btn'),
                        data=result['text'],
                        file_name=f"transcript_{uploaded_file.name}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"{t('error')} {str(e)}")
            
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

else:
    st.info(t('upload_prompt'))
    st.markdown(t('use_cases'))
    c1, c2, c3 = st.columns(3)
    c1.markdown(t('use_case_1'))
    c2.markdown(t('use_case_2'))
    c3.markdown(t('use_case_3'))
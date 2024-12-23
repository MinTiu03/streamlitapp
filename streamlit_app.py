import streamlit as st

st.navigation(
    [
        st.Page(
            "pages/grabcut.py",
            title="1. Ứng dụng tách nền bằng thuật toán GrabCut",
        ),
        st.Page(
            "pages/watershed.py",
            title="2. Phân đoạn ký tự bằng Watershed Segmentation",
        ),
        st.Page(
            "pages/haar_knn.py",
            title="3. Phát hiện khuôn mặt với Haar Features và KNN",
        ),
        st.Page(
            "pages/face_verification.py",
            title="4. Ứng dụng xác nhận khuôn mặt",
        ),
        st.Page(
            "pages/keypoint_detection.py",
            title="5. Phát hiện Keypoint trên Synthetic Shapes Dataset",
        ),
        st.Page(
            "pages/keypoint_matching.py",
            title="6. So khớp Keypoint dựa trên tiêu chí Rotation",
        ),
        st.Page(
            "pages/instance_search.py",
            title="7. Tìm kiếm ảnh chứa đối tượng truy vấn",
        ),
        st.Page(
            "pages/tracking.py",
            title="8. Theo dõi đối tượng (SOT) bằng thuật toán KCF",
        ),
        st.Page(
            "pages/sort_mot.py",
            title="9. Thuật toán SORT (Simple Online Realtime Tracking)",
        ),
        st.Page(
            "pages/handwriting_letter_recognition.py",
            title="10. Nhận dạng chữ viết tay",
        ),
        st.Page(
            "pages/processing_image.py",
            title="11. Ứng dụng xử lý ảnh"
        )
    ]
).run()

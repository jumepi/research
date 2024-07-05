import cv2

def capture_reference_image():
    # カメラをキャプチャするためのオブジェクトを作成
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラを開けませんでした。")
        return

    print("基準画像をキャプチャする準備ができました。")
    print("スペースキーを押して基準画像をキャプチャし、保存します。")

    while True:
        # カメラからフレームを読み取る
        ret, frame = cap.read()

        if not ret:
            print("フレームを読み取れませんでした。")
            break

        # 画像を表示
        cv2.imshow('Capture Reference Image', frame)

        # スペースキーを押すとフレームを基準画像として保存
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite('reference_image.jpg', frame)
            print("基準画像を保存しました。")
            break

        # 'q'キーが押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # リソースを解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_reference_image()

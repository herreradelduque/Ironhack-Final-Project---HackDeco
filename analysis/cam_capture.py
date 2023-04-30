import cv2


def capture():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)

    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(filename='./data/img_users/img.jpg', img=frame)
                webcam.release()
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                break
            elif key == ord('q'):
                print("Turning off camera")
                webcam.release()
                print("Camera off")
                print("Program ended")
                cv2.destroyAllWindows()
                cv2.waitKey(1)

                break

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break

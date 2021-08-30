import os
import traceback

import extract_msg
import PySimpleGUI as sg

import logger
from config import LOGS_PATH

# Initialize logger
if not os.path.exists(LOGS_PATH):
    os.makedirs(os.path.dirname(LOGS_PATH))

log = logger.setup_logger(file_name=LOGS_PATH)


def main(msg_file_path, output_folder_path):
    msg_file_name = os.path.splitext(os.path.basename(msg_file_path))[0]
    final_output_folder_path = os.path.join(output_folder_path, msg_file_name)
    attachments_folder_path = os.path.join(final_output_folder_path, "attachments")

    try:
        print("Extracting data from: ", msg_file_name)

        # Creating output folder
        if not os.path.exists(final_output_folder_path):
            os.makedirs(final_output_folder_path)
            os.mkdir(attachments_folder_path)

        msg_obj = extract_msg.Message(msg_file_path)
        msg_sender = "Sender: " + str(msg_obj.sender) + "\n\n"
        msg_date = "Date: " + str(msg_obj.date) + "\n\n"
        msg_subject = "Subject: " + str(msg_obj.subject) + "\n\n"
        msg_message = "Message: " + str(msg_obj.body) + "\n\n"

        # Writing to txt file
        output_file = open(os.path.join(final_output_folder_path, "data.txt"), "a")
        output_file.write(msg_sender)
        output_file.write(msg_date)
        output_file.write(msg_subject)
        output_file.write(msg_message)
        output_file.close()

        # Saving attachments
        msg_obj.save_attachments(customPath=attachments_folder_path)

        print("Extraction successfull")
        print(" ")
    except Exception:
        print("Error encountered, please check logs")
        log.error(traceback.format_exc())


if __name__ == "__main__":
    try:
        # Setting theme
        sg.theme("Reddit")
        font = ("Calibri", 12)

        # GUI Layout
        gui_layout = [
            [
                sg.Text("Select .msg file", size=(20, 1), font=font),
                sg.In(size=(50, 1), enable_events=True, key="-MSG_PATH-", font=font),
                sg.FileBrowse(file_types=(("MSG Files", "*.msg"),)),
            ],
            [
                sg.Text("Select output folder", size=(20, 1), font=font),
                sg.In(
                    size=(50, 1), enable_events=True, key="-OUTPUT_FOLDER-", font=font
                ),
                sg.FolderBrowse(),
            ],
            [
                [sg.Text("Output:", font=font)],
                sg.Output(
                    size=(77, 20),
                    background_color="black",
                    text_color="white",
                    key="-OUTPUT-",
                    font=font,
                ),
            ],
            [
                sg.Button(button_text="Run", key="-RUN-"),
                sg.Cancel(),
            ],
        ]

        gui_window = sg.Window("Py-MSG-Reader", gui_layout)

        while True:
            event, values = gui_window.read(timeout=100)

            if event == sg.WIN_CLOSED or event == "Cancel":
                break

            if event == "-RUN-":
                msg_file_path = values["-MSG_PATH-"]
                output_folder_path = values["-OUTPUT_FOLDER-"]

                if msg_file_path and output_folder_path:
                    # Processing file
                    print("Py-MSG-Reader")
                    main(msg_file_path, output_folder_path)
                else:
                    print("Please select the .msg file and output folder")

    except Exception:
        log.error(traceback.format_exc())

    main()

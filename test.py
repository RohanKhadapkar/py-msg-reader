import extract_msg

file_path = r"data\25900830.msg"

msg = extract_msg.Message(file_path)
msg_sender = msg.sender
msg_date = msg.date
msg_subj = msg.subject
msg_message = msg.body
msg.save_attachments(customPath="data\output")

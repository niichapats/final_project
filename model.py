person_table_model = {
  'ID': '',
  'fist': '',
  'last': '',
  'type': '',
}

login_table_model = {
  'ID': '',
  'username': '',
  'password': '',
  'role': '',
}

project_table_model = {
  'ProjectID': '',
  'Title': '',
  'Lead': '',
  'Member1': '',
  'Member2': '',
  'Advisor': '',
  'Status': '',
}

advisor_pending_request_table_model = {
  'ProjectID': '',
  'to_be_advisor': '',
  'Response': '',
  'Response_date': '',
}

member_pending_request_table_model = {
  'ProjectID': '',
  'to_be_member': '',
  'Response': '',
  'Response_date': '',
}

proposal_project_table_model = {
  'ProjectID': '',
  'Lead': '',
  'Advisor': '',
  'Proposal': '',
  'Status': '',
}

evaluate_project_table_model = {
  'ProjectID': '',
  'Lead': '',
  'Advisor': '',
  'Project': '',
  'Evaluator': '',
  'Status': '',
}

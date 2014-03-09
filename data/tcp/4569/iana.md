_Name:_ iax

_Description:_ Inter-Asterisk eXchange

_Note:_ Defined TXT keys:<br/>
  auth          plaintext | md5 | rsakeys<br/>
  userid        alphanumeric, additionally '_', '+', '-'<br/>
  secret        any printable ASCII characters<br/>
  domain        any DNS domain name or IP address<br/>
  extension     alphanumeric, additionally '*', '#', '_', '+', '-'<br/>
  context       alphanumeric, additionally '_', '+', '-'<br/>
  trunk         yes | no | 0 | 1<br/>
  welcome       alphanumeric, additionally '*', '#', '_', '+', '-'<br/>
  voicemail     alphanumeric, additionally '*', '#', '_', '+', '-'<br/>
  reception     alphanumeric, additionally '*', '#', '_', '+', '-'<br/>
  echotest      alphanumeric, additionally '*', '#', '_', '+', '-'<br/>
  ivrtest       alphanumeric, additionally '*', '#', '_', '+', '-'<br/>
All of these TXT record keys are optional, they may be omitted.
Further keys may be added in the future.


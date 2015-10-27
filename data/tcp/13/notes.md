[RFC 867](https://tools.ietf.org/html/rfc867) defines the Daytime protocol.

... daytime service is defined as a connection based application on
TCP.  A server listens for TCP connections on TCP port 13.  Once a
connection is established the current date and time is sent out the connection as a ascii character string (and any data received is
thrown away).  The service closes the connection after sending the quote.

See also [UDP/13](/view/udp/13) for the UDP version of this protocol.


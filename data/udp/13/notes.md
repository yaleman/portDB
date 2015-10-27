[RFC 867](https://tools.ietf.org/html/rfc867) defines the Daytime protocol.

... daytime service service is defined as a datagram based
application on UDP.  A server listens for UDP datagrams on UDP port
13.  When a datagram is received, an answering datagram is sent
containing the current date and time as a ASCII character string (the
data in the received datagram is ignored).

See also [TCP/13](/view/tcp/13) for the TCP version of this protocol.

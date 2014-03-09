_Name:_ www-http

_Description:_ World Wide Web HTTP

_Note:_ This is a duplicate of the "http" service and should not be used for discovery purposes.
      u=&lt;username&gt; p=&lt;password&gt; path=&lt;path to document&gt;
      (see txtrecords.html#http)
      Known Subtypes: _printer
      NOTE: The meaning of this service type, though called just "http", actually
      denotes something more precise than just "any data transported using HTTP".
      The DNS-SD service type "http" should only be used to advertise content that:
      * is served over HTTP,
      * can be displayed by "typical" web browser client software, and
      * is intented primarily to be viewed by a human user.
      Of course, the definition of "typical web browser" is subjective, and may
      change over time, but for practical purposes the DNS-SD service type "http"
      can be understood as meaning "human-readable HTML content served over HTTP".
      In some cases other widely-supported content types may also be appropriate,
      such as plain text over HTTP, or JPEG image over HTTP.
      Content types not intented primarily for viewing by a human user, or not
      widely-supported in web browsing clients, should not be advertised as
      DNS-SD service type "http", even if they do happen to be transported over HTTP.
      Such types should be advertised as their own logical service type with their
      own DNS-SD service type, for example, XUL (XML User Interface Language)
      transported over HTTP is advertised explicitly as DNS-SD service type "xul-http".


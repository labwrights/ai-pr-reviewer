Make add_ticket never crash the page

A database hiccup used to show the user an error page. Now add_ticket just returns -1 and the page carries on.

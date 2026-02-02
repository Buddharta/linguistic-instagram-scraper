#!/usr/bin/env python3
import instaloader
#instance
l=instaloader.Instaloader()
#loading session
l.login(USER,PASSWORD)
l.interactive_login(USER)
l.load_session_from_file(USER)

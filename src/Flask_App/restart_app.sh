#!/bin/bash
sudo systemctl daemon-reload && sudo systemctl restart flaskapp && sudo systemctl enable flaskapp && sudo systemctl status flaskapp

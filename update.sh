#!/bin/sh
pid=`ps aux | grep weekly_config.xml | grep -v grep | awk '{print $2}'`
sudo kill ${pid}
sudo uwsgi -x weekly_config.xml

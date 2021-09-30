import gitlab
import urllib3
import re

#vars
userid= {{Userid}}
gitLabToken = "{{Token}}"
gitLabUrl = "{{GitLabUrl}}"


#gitlab connection
gl = gitlab.Gitlab( gitLabUrl, private_token=gitLabToken)


#list of groups id is lgi
groups = gl.groups.list(all=True)
lgi = re.findall("\d+", str(groups))


#add user
for i in lgi:
    group = gl.groups.get(i)
    if group.members.get(userid).id == userid:
      continue
    else:
        member = group.members.create({'user_id': userid,'access_level': gitlab.REPORTER_ACCESS})

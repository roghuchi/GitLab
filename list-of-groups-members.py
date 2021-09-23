import gitlab
import re
import xlwt
from xlwt import Workbook


# make a workbook
wb = Workbook()
sheet1 = wb.add_sheet('Groups')
sheet1.write(0, 0, 'id')
sheet1.write(0, 1, 'groups')
sheet1.write(0, 2, 'members') 


#vars
gitLabToken = "{{Token}}"
gitLabUrl = "{{GitLabUrl}}"


#gitlab connection
gl = gitlab.Gitlab( gitLabUrl, private_token=gitLabToken)


#list of groups id is lgi
groups = gl.groups.list(all=True)
lgi = re.findall("\d+", str(groups))
index1 = 0
while index1 < len(lgi):
    try:
        
        group = gl.groups.get(lgi[index1])
        rexResult1 = re.search(r"path_with_namespace': '([^']+).*visibility': '([^']+)", str(group))
        pathWithNamespace = rexResult1.group(1)
        visibility = rexResult1.group(2)
        members = group.members.all(all=True)
        g =pathWithNamespace + " - " + visibility
        
        # list of members id is lgi
        lmi = re.findall("\d+", str(members))
        
        # list of members with access level for one group
        i = index1+1
        sheet1.write(i, 0, lgi[index1])
        sheet1.write(i, 1, g)
        index1 = index1 + 1
        index2 = 0
        j = 2
        while index2 < len(lmi):
            try:
                member = group.members.get(lmi[index2])
                rexResult2 = re.search(r"username': '([^']+).*'state': 'active'.*access_level': ([^,]+)", str(member))
                userName = rexResult2.group(1)
                accessLevel = rexResult2.group(2)
                m = userName + " - "+ accessLevel
                sheet1.write(i, j, m)
                j = j+1
                index2 = index2 + 1
                continue
            except:
                index2 = index2 + 1
                continue
    except:
        index1 = index1 + 1
        continue

wb.save('glist.xls') 

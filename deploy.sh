git init
git remote rm origin
git config --global user.email "2380540710@qq.com"
git config --global user.name "chenxuefan"
git remote add origin https://github.com/chenxuefan/sziit-scores.search.git
git add .
git commit -m "update"
git pull origin master
git push -u origin +master
# 社团活动（Django 课后任务）

按课件要求实现的活动管理小站：活动列表、添加、编辑、删除，按标题搜索，开始时间校验。

## 运行

课程虚拟环境在 `D:\Coding\PY\.venv`（Django 6.1.3），可以直接用它的 Python：

```bash
cd D:\Coding\PY\Week2\DjangoProject
D:\Coding\PY\.venv\Scripts\python.exe manage.py migrate
D:\Coding\PY\.venv\Scripts\python.exe manage.py runserver
```

浏览器打开 <http://127.0.0.1:8000/>。

数据库里已放 3 条演示数据；想从空库开始，删除 `db.sqlite3` 后重新执行 `migrate`。
需要后台管理的话，先 `python manage.py createsuperuser`，再访问 `/admin/`。

## 三项课后任务对应位置

| 任务 | 位置 |
| --- | --- |
| ① 活动的「编辑」与「删除」页面，复用 ModelForm 完整流程 | `activities/views.py` 的 `activity_update` / `activity_delete`；`activities/templates/activities/activity_form.html`、`activity_confirm_delete.html` |
| ② 表单校验：开始时间不得早于当前时间 | `activities/forms.py` 的 `ActivityForm.clean_start_time` |
| ③ 列表页按标题关键词搜索 | `activities/views.py` 的 `activity_list`（`q` 参数 + `title__icontains`）；`activity_list.html` 的搜索框 |

编辑页和添加页共用 `ActivityForm`：编辑时传 `instance=activity`，`form.save()` 直接更新原记录。
删除页先 GET 到确认页，确认后 POST 才真正删除。

## 结构

```
DjangoProject/
├── manage.py
├── DjangoProject/          # 项目配置
│   ├── settings.py         # 已注册 activities，时区 Asia/Shanghai
│   └── urls.py             # path('', include('activities.urls'))
└── activities/
    ├── models.py           # Activity：标题、开始时间、地点、说明
    ├── forms.py            # ActivityForm（ModelForm + 时间校验）
    ├── views.py            # 列表 / 新增 / 编辑 / 删除
    ├── urls.py
    ├── admin.py
    ├── tests.py            # 9 个测试
    └── templates/activities/
        ├── base.html
        ├── activity_list.html
        ├── activity_form.html
        └── activity_confirm_delete.html
```

## 测试

```bash
python manage.py test
```

覆盖：过去时间被拒绝 / 未来时间通过、按标题过滤、关键词为空时显示全部、新增、编辑、删除确认页、删除。

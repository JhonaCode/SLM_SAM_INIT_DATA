import pandas as pd

hi=00
hf=23
dates =[
        ["2014-02-27T%s"%hi,"2014-02-27T%s"%hf],#days.feb27, #*01
        #["2014-03-06T%s"%hi,"2014-03-06T%s"%hf],#days.mar06, #02
        ["2014-03-09T%s"%hi,"2014-03-09T%s"%hf],#days.mar09, #03
        ["2014-03-10T%s"%hi,"2014-03-10T%s"%hf],#days.mar10, #04
        ["2014-03-15T%s"%hi,"2014-03-15T%s"%hf],#days.mar15, #05
        ["2014-03-16T%s"%hi,"2014-03-16T%s"%hf],#days.mar16, #06
        ["2014-03-17T%s"%hi,"2014-03-17T%s"%hf],#days.mar17, #07
        ["2014-03-18T%s"%hi,"2014-03-18T%s"%hf],#days.mar18, #08
        ["2014-09-02T%s"%hi,"2014-09-02T%s"%hf],#days.sep02, #09
        ["2014-09-03T%s"%hi,"2014-09-03T%s"%hf],#days.sep03, #10
        ["2014-09-04T%s"%hi,"2014-09-04T%s"%hf],#days.sep04, #11
        ["2014-09-09T%s"%hi,"2014-09-09T%s"%hf],#days.sep09, #12
        ["2014-09-11T%s"%hi,"2014-09-11T%s"%hf],#days.sep11, #13
        ["2014-09-14T%s"%hi,"2014-09-14T%s"%hf],#days.sep14, #14
        ["2014-09-15T%s"%hi,"2014-09-15T%s"%hf],#days.sep15, #15
        ["2014-09-16T%s"%hi,"2014-09-16T%s"%hf],#days.sep16, #16
        ["2014-09-19T%s"%hi,"2014-09-19T%s"%hf],#days.sep19, #17
        ["2014-09-20T%s"%hi,"2014-09-20T%s"%hf],#days.sep20, #18
        ["2014-09-21T%s"%hi,"2014-09-21T%s"%hf],#days.sep21, #19
        ["2014-09-22T%s"%hi,"2014-09-22T%s"%hf],#days.sep22, #20
        ["2014-09-23T%s"%hi,"2014-09-23T%s"%hf],#days.sep23, #21
        ["2014-09-26T%s"%hi,"2014-09-26T%s"%hf],#days.sep26, #22
        ["2014-09-27T%s"%hi,"2014-09-27T%s"%hf],#days.sep27, #23
        ["2014-09-29T%s"%hi,"2014-09-29T%s"%hf],#days.sep29, #24
        ["2014-10-01T%s"%hi,"2014-10-01T%s"%hf],#days.oct01, #25
        ["2014-10-03T%s"%hi,"2014-10-03T%s"%hf],#days.oct03, #26
        ["2014-10-05T%s"%hi,"2014-10-05T%s"%hf],#days.oct05, #27
        ["2014-10-07T%s"%hi,"2014-10-07T%s"%hf],#days.oct07, #28
        ["2014-10-08T%s"%hi,"2014-10-08T%s"%hf],#days.oct08, #29
        ["2014-10-09T%s"%hi,"2014-10-09T%s"%hf],#days.oct09, #*30
]

date_format = '%Y-%m-%dT%H'

days=[]
for d in dates:

    days.append([pd.to_datetime(d[0],format=date_format),pd.to_datetime(d[1],format=date_format)])




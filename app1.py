import urllib.request
import streamlit as st
import pendulum as pdlm
from io import StringIO
import datetime
import pytz
from contextlib import contextmanager, redirect_stdout
import kinqimen
from kinliuren import kinliuren
import config

#BASE_URL_KINLIUREN = 'https://raw.githubusercontent.com/kentang2017/kinliuren/master/'

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write
        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        stdout.write = new_write
        yield

st.set_page_config(layout="wide",page_title="奇門遁甲排盘-wzs test 202504")
pan,log = st.tabs([' 🧮排盤 ',' ' ])
with st.sidebar:
    pp_date=st.date_input("日期",pdlm.now(tz='Asia/Shanghai').date())
    pp_time = st.text_input('輸入時間(如: 18:30)', '')
    option = st.selectbox( '起盤方式', ( ' 時家奇門 ', ' 刻家奇門 '))
    option2 = st.selectbox( '排盤', (' 置閏 ',' 拆補 '))
    num = dict(zip([' 時家奇門 ', ' 刻家奇門 '],[1,2])).get(option)
    pai = dict(zip([' 拆補 ',' 置閏 '],[1,2])).get(option2)
    p = str(pp_date).split("-")
    pp = str(pp_time).split(":")
    y = int(p[0])
    m = int(p[1])
    d = int(p[2])
    try:
        h = int(pp[0])
        mintue = int(pp[1])
    except ValueError:
        pass
    manual = st.button('起盤')
    instant = st.button('即時')
   

with pan:
    st.header('堅奇門')
    eg = list("巽離坤震兌艮坎乾")
    now = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong'))
    ny = now.year
    nm = now.month
    nd = now.day
    nh = now.hour
    nmintue = now.minute
    nj_q =  config.jq(ny,nm,nd,nh,nmintue)
    ngz = config.gangzhi(ny,nm,nd,nh,nmintue)
    nqtext = kinqimen.Qimen(ny,nm,nd,nh,nmintue).pan(pai)
    nlunar_month = dict(zip(range(1,13), config.cmonth)).get(config.lunar_date_d(ny,nm,nd).get("月"))
    nlr = kinliuren.Liuren( nqtext.get("節氣"),nlunar_month, ngz[2], ngz[3]).result(0)
    nqd = [nqtext.get("地盤").get(i) for i in eg]
    ne_to_s = nlr.get("地轉天盤")
    ne_to_g = nlr.get("地轉天將")
    nqt = [nqtext.get('天盤', {}).get(i) for i in eg]
    ngod = [nqtext.get("神").get(i) for i in eg]
    ndoor = [nqtext.get("門").get(i) for i in eg]
    nstar = [nqtext.get("星").get(i) for i in eg]
    nmd = nqtext.get("地盤").get("中")
    output2 = st.empty()
    with st_capture(output2.code):
        if not manual:
            print("時家奇門 | {}".format(nqtext.get("排盤方式")))
            print("{}年{}月{}日{}時\n".format(ny,nm,nd,nh))
            print("{} |\n{} | 節氣︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(nqtext.get("干支"), nqtext.get("排局"),  nj_q,  nqtext.get("值符值使").get("值符星宮")[0]+"-"+nqtext.get("值符值使").get("值符星宮")[1], nqtext.get("值符值使").get("值使門宮")[0]+"門"+nqtext.get("值符值使").get("值使門宮")[1]+"宮" ))
            print("農曆月：{} | 節氣日數差距：{}天\n".format(config.lunar_date_d(ny, nm, nd).get("農曆月"),config.qimen_ju_name_zhirun_raw(ny, nm, nd, nh, nmintue).get("距節氣差日數")))
            print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(ne_to_s.get("巳"),ne_to_g.get("巳"),ne_to_s.get("午"),ne_to_g.get("午"),ne_to_s.get("未"),ne_to_g.get("未"),ne_to_s.get("申"),ne_to_g.get("申")))
            print("  ＼────────┴──┬─────┴─────┬──┴────────／")
            print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(ngod[0], ngod[1], ngod[2]))
            print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(ndoor[0], nqt[0], ndoor[1], nqt[1], ndoor[2], nqt[2]))
            print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(nstar[0], nqd[0], nstar[1], nqd[1], nstar[2], nqd[2]))
            print(" {}├───────────┼───────────┼───────────┤{}".format(ne_to_s.get("辰"),ne_to_s.get("酉")))
            print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(ne_to_g.get("辰"),ngod[3], ngod[4],ne_to_g.get("酉")))
            print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(ndoor[3], nqt[3],  ndoor[4], nqt[4]))
            print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(nstar[3], nqd[3], nmd, nstar[4], nqd[4]))
            print(" 　├───────────┼───────────┼───────────┤")
            print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(ngod[5], ngod[6], ngod[7]))
            print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(ne_to_s.get("卯"),ndoor[5], nqt[5], ndoor[6], nqt[6], ndoor[7], nqt[7], ne_to_s.get("戌")))
            print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(ne_to_g.get("卯"),nstar[5], nqd[5], nstar[6], nqd[6], nstar[7], nqd[7], ne_to_g.get("戌")))
            print("  ／────────┬──┴─────┬─────┴──┬────────＼")
            print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(ne_to_s.get("寅"),ne_to_g.get("寅"),ne_to_s.get("丑"),ne_to_g.get("丑"),ne_to_s.get("子"),ne_to_g.get("子"),ne_to_s.get("亥"),ne_to_g.get("亥")))
            expander = st.expander("原始碼")
            expander.write(str(nqtext))
        if manual:
            gz = config.gangzhi(y,m,d,h,mintue)
            j_q =  config.jq(y, m, d, h, mintue)
            lunar_month = dict(zip(range(1,13), config.cmonth)).get(config.lunar_date_d(y,m,d).get("月"))
            if num == 1:
                qtext = kinqimen.Qimen(y,m,d,h,mintue).pan(pai)
                lr = kinliuren.Liuren( qtext.get("節氣"),lunar_month, gz[2], gz[3]).result(0)
                qd = [qtext.get("地盤").get(i) for i in eg]
                e_to_s = lr.get("地轉天盤")
                e_to_g = lr.get("地轉天將")
                qt = [qtext['天盤'].get(i) for i in eg]
                god = [qtext.get("神").get(i) for i in eg]
                door = [qtext.get("門").get(i) for i in eg]
                star = [qtext.get("星").get(i) for i in eg]
                md = qtext.get("地盤").get("中")
                print("時家奇門 | {}".format(qtext.get("排盤方式")))
                print("{}年{}月{}日{}時\n".format(y,m,d,h))
                print("{} |\n{} | 節氣︰{} |\n值符天干︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext.get("干支"), qtext.get("排局"),  j_q, qtext.get("值符值使").get("值符天干")[0]+qtext.get("值符值使").get("值符天干")[1],  qtext.get("值符值使").get("值符星宮")[0]+"-"+qtext.get("值符值使").get("值符星宮")[1], qtext.get("值符值使").get("值使門宮")[0]+"門"+qtext.get("值符值使").get("值使門宮")[1]+"宮" ))
                print("農曆月：{} | 節氣日數差距：{}天\n".format(config.lunar_date_d(y, m, d).get("農曆月"),config.qimen_ju_name_zhirun_raw(y,m,d,h,mintue).get("距節氣差日數")))
                print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳"),e_to_g.get("巳"),e_to_s.get("午"),e_to_g.get("午"),e_to_s.get("未"),e_to_g.get("未"),e_to_s.get("申"),e_to_g.get("申")))
                print("  ＼────────┴──┬─────┴─────┬──┴────────／")
                print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
                print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
                print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
                print(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰"),e_to_s.get("酉")))
                print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰"),god[3], god[4],e_to_g.get("酉")))
                print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
                print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
                print(" 　├───────────┼───────────┼───────────┤")
                print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
                print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯"),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌")))
                print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯"),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌")))
                print("  ／────────┬──┴─────┬─────┴──┬────────＼")
                print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅"),e_to_g.get("寅"),e_to_s.get("丑"),e_to_g.get("丑"),e_to_s.get("子"),e_to_g.get("子"),e_to_s.get("亥"),e_to_g.get("亥")))
                expander = st.expander("原始碼")
                expander.write(str(qtext))
            if num == 2:
                qtext_m = kinqimen.Qimen(y,m,d,h,mintue).pan_minute(pai)
                lr = kinliuren.Liuren( qtext_m.get("節氣"),lunar_month, gz[3], gz[4]).result(0)
                qd = [qtext_m.get("地盤").get(i) for i in eg]
                e_to_s = lr.get("地轉天盤")
                e_to_g = lr.get("地轉天將")
                qt = [qtext_m.get("天盤").get(i) for i in eg]
                god = [qtext_m.get("神").get(i) for i in eg]
                door = [qtext_m.get("門").get(i) for i in eg]
                star = [qtext_m.get("星").get(i) for i in eg]
                md = qtext_m.get("地盤").get("中")
                print("刻家奇門 | {}".format(qtext_m.get("排盤方式")))
                print("{}年{}月{}日{}時\n".format(y,m,d,h))
                print("{} |\n{} | 節氣︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext_m.get("干支"), qtext_m.get("排局"),  j_q,  qtext_m.get("值符值使").get("值符星宮")[0]+"-"+qtext_m.get("值符值使").get("值符星宮")[1], qtext_m.get("值符值使").get("值使門宮")[0]+"門"+qtext_m.get("值符值使").get("值使門宮")[1]+"宮" ))
                print("農曆月：{} | 節氣日數差距：{}天\n".format(config.lunar_date_d(y, m, d).get("農曆月"),config.qimen_ju_name_zhirun_raw(y,m,d,h,mintue).get("距節氣差日數")))
                print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳"),e_to_g.get("巳"),e_to_s.get("午"),e_to_g.get("午"),e_to_s.get("未"),e_to_g.get("未"),e_to_s.get("申"),e_to_g.get("申")))
                print("  ＼────────┴──┬─────┴─────┬──┴────────／")
                print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
                print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
                print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
                print(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰"),e_to_s.get("酉")))
                print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰"),god[3], god[4],e_to_g.get("酉")))
                print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
                print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
                print(" 　├───────────┼───────────┼───────────┤")
                print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
                print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯"),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌")))
                print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯"),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌")))
                print("  ／────────┬──┴─────┬─────┴──┬────────＼")
                print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅"),e_to_g.get("寅"),e_to_s.get("丑"),e_to_g.get("丑"),e_to_s.get("子"),e_to_g.get("子"),e_to_s.get("亥"),e_to_g.get("亥")))
                expander = st.expander("原始碼")
                expander.write(str(qtext_m))

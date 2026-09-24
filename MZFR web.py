import datetime
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="မဟာဇနက္က အနာဂတ်ဟောကိန်း",
    page_icon="🔮",
    layout="centered"
)

# App Title & Description
st.title("🔮 မဟာဇနက္က အနာဂတ်ဟောကိန်း")
st.write("မွေးနေ့ရက်နှင့် မွေးသက္ကရာဇ်ကို ထည့်သွင်း၍ သင့်ဘဝ၏ အနာဂတ် ကံဇာတာ အနိမ့်အမြင့်များကို တွက်ချက်ကြည့်ပါ။")

st.divider()

# ဇနက အဆင့် (၆) ခုနှင့် အဓိပ္ပာယ်များ
stage_meanings = {
    1: "ပြင်ဆင်ခြင်းအဆင့်",
    2: "စတင်စွန့်စားခြင်းအဆင့်",
    3: "စိန်ခေါ်မှုနှင့် အခက်အခဲချိန်",
    4: "ပြန်လည်တည်ငြိမ်လာချိန်",
    5: "အကြီးမားဆုံး အောင်မြင်မှုချိန်",
    6: "အေးချမ်းသာယာသောအချိန်"
}

day_starts = {
    "တနင်္ဂနွေ (Sunday)": 1,
    "တနင်္လာ (Monday)": 2,
    "အင်္ဂါ (Tuesday)": 3,
    "ဗုဒ္ဓဟူး (Wednesday)": 4,
    "ကြာသပတေး (Thursday)": 5,
    "သောကြာ (Friday)": 6,
    "စနေ (Saturday)": 7
}

# User Inputs UI
col1, col2 = st.columns(2)

with col1:
    selected_day_label = st.selectbox(
        "မွေးနေ့ရက် ရွေးချယ်ပါ-",
        list(day_starts.keys())
    )

with col2:
    current_year = datetime.datetime.now().year
    years_list = list(range(current_year - 1, 1899, -1))
    default_index = years_list.index(2000) if 2000 in years_list else 0

    birth_year = st.selectbox(
        "မွေးသက္ကရာဇ် (ခရစ်နှစ်) ရွေးချယ်ပါ-",
        years_list,
        index=default_index
    )

# Calculation Logic
if st.button("ဟောကိန်း တွက်ချက်မည်", type="primary"):
    with st.spinner("တွက်ချက်နေပါသည်..."):
        age = current_year - birth_year
        start_num = day_starts[selected_day_label]
        is_odd_start = (start_num % 2 != 0)

        # Matrix Logic Calculation for Current State
        if is_odd_start:
            if age % 2 == 0:
                curr_col = ((age // 2) - 1) % 6 + 1
                is_middle = True
            else:
                curr_col = (age // 2) % 6 + 1
                is_middle = False
        else:
            if age % 2 != 0:
                curr_col = ((age // 2) - 1) % 6 + 1
                is_middle = True
            else:
                curr_col = (age // 2) % 6 + 1
                is_middle = False

        next_col = (curr_col % 6) + 1

        # Dynamic Age Finder Function
        def find_age_for_col(target_col, start_from_age, include_current=False):
            check_age = start_from_age if include_current else start_from_age + 1
            while True:
                if is_odd_start:
                    if check_age % 2 != 0 and ((check_age // 2) % 6 + 1) == target_col:
                        return check_age
                else:
                    if check_age % 2 == 0 and (((check_age // 2) - 1) % 6 + 1) == target_col:
                        return check_age
                check_age += 1

        st.subheader("📊 တွက်ချက်ရရှိသော ရလဒ်")
        st.info(f"**မွေးနေ့ရက်:** {selected_day_label} | **မွေးသက္ကရာဇ်:** {birth_year} | **လက်ရှိအသက်:** {age} နှစ်")

        # Status Message
        if is_middle:
            status_text = f"အသက် **{age}** နှစ်သည် **{stage_meanings[curr_col]}** နှင့် **{stage_meanings[next_col]}** တို့၏ အကူးအပြောင်း အလယ်ဗဟိုတွင် ရှိနေပါသည်။"
        else:
            status_text = f"အသက် **{age}** နှစ်သည် **{stage_meanings[curr_col]}** တွင် ရောက်ရှိနေပါသည်။"

        st.markdown(f"**အခြေအနေ:** {status_text}")

        # Dynamic Timeline Logic (Fixed to always display stabilization)
        is_in_unluck = (curr_col == 3) or (is_middle and next_col == 3)
        is_in_luck = (curr_col in [5, 6]) or (is_middle and next_col in [5, 6])
        is_in_stab = (curr_col == 4) or (is_middle and next_col == 4)

        st.divider()
        st.subheader("✨ အနာဂတ် ဟောကိန်း သုံးသပ်ချက်")

        if is_in_unluck:
            recovery_age = find_age_for_col(4, age, include_current=False)
            luck_start_age = find_age_for_col(5, recovery_age, include_current=True)
            luck_end_age = find_age_for_col(6, luck_start_age, include_current=False)
            
            st.warning(f"လက်ရှိတွင် အခက်အခဲနှင့် စိန်ခေါ်မှုများ ကြုံတွေ့ရနိုင်သော်လည်း အသက် **{recovery_age}** နှစ်တွင် ကံဇာတာ ပြန်လည်တည်ငြိမ်လာမည် ဖြစ်ပါသည်။")
            st.success(f"ထို့နောက် အနီးဆုံး အကောင်းဆုံး ကံဇာတာနှင့် တောက်ပသော အောင်မြင်မှုများကို အသက် **{luck_start_age}** နှစ်မှ **{luck_end_age}** နှစ်အတွင်း စတင် ရရှိလာပါလိမ့်မည်။")

        elif is_in_stab:
            luck_start_age = find_age_for_col(5, age, include_current=False)
            luck_end_age = find_age_for_col(6, luck_start_age, include_current=False)
            
            st.info(f"လက်ရှိတွင် အခက်အခဲများမှ **ပြန်လည်တည်ငြိမ်လာသော အချိန် (အသက် {age} နှစ်)** ၌ ရောက်ရှိနေပါသည်။")
            st.success(f"ရှေ့ဆက်၍ အနီးဆုံး အကောင်းဆုံး ကံဇာတာနှင့် တောက်ပသော အောင်မြင်မှုများကို အသက် **{luck_start_age}** နှစ်မှ **{luck_end_age}** နှစ်အတွင်း ရရှိလာပါလိမ့်မည်။")

        elif is_in_luck:
            luck_end_age = find_age_for_col(6, age, include_current=True)
            unluck_age = find_age_for_col(3, luck_end_age, include_current=False)
            recovery_age = find_age_for_col(4, unluck_age, include_current=False)
            
            st.success(f"လက်ရှိတွင် အကောင်းဆုံး ကံဇာတာနှင့် တောက်ပသော အောင်မြင်မှုကာလအတွင်း ရောက်ရှိနေပြီး အသက် **{luck_end_age}** နှစ်အထိ အေးချမ်းသာယာမှုများကို ရရှိခံစားရပါလိမ့်မည်။")
            st.warning(f"ရှေ့ဆက်၍ အသက် **{unluck_age}** နှစ်တွင် စိန်ခေါ်မှုနှင့် အခက်အခဲများ ကြုံတွေ့ရနိုင်ပြီး အသက် **{recovery_age}** နှစ်တွင် ပြန်လည်တည်ငြိမ်လာပါမည်။")

        else:
            unluck_age = find_age_for_col(3, age, include_current=False)
            recovery_age = find_age_for_col(4, unluck_age, include_current=False)
            luck_start_age = find_age_for_col(5, recovery_age, include_current=True)
            luck_end_age = find_age_for_col(6, luck_start_age, include_current=False)

            if unluck_age < luck_start_age:
                st.warning(f"ရှေ့ဆက်၍ အသက် **{unluck_age}** နှစ်တွင် စိန်ခေါ်မှုနှင့် အခက်အခဲများ ကြုံတွေ့ရနိုင်ပါသည်။")
                st.info(f"ထိုအခက်အခဲများသည် အသက် **{recovery_age}** နှစ်တွင် စတင် **ပြန်လည်တည်ငြိမ် လျော့ပါးလာမည်** ဖြစ်ပါသည်။")
                st.success(f"ထို့နောက် အကောင်းဆုံး ကံဇာတာနှင့် တောက်ပသော အောင်မြင်မှုများကို အသက် **{luck_start_age}** နှစ်မှ **{luck_end_age}** နှစ်အတွင်း ရရှိလာပါလိမ့်မည်။")
            else:
                st.success(f"အနီးဆုံး အကောင်းဆုံး ကံဇာတာနှင့် တောက်ပသော အောင်မြင်မှုများကို အသက် **{luck_start_age}** နှစ်မှ **{luck_end_age}** နှစ်အတွင်း စတင် ရရှိလာပါလိမ့်မည်။")
                st.warning(f"ထို့နောက် အသက် **{unluck_age}** နှစ်တွင် စိန်ခေါ်မှုနှင့် အခက်အခဲများ ကြုံတွေ့ရနိုင်ပြီး အသက် **{recovery_age}** နှစ်တွင် ပြန်လည်တည်ငြိမ်လာပါမည်။")

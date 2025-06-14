import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import cvxpy as cp
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="منصة الحوكمة المتقدمة", layout="wide")

st.markdown("""
<style>
* {direction: rtl; text-align: right;}
</style>
""", unsafe_allow_html=True)

st.title("📊 منصة محاكاة وتقييم الحوكمة المتقدمة في البنوك التشاركية")
st.markdown("💡 هذه المنصة تفاعلية تساعد على قياس جودة الحوكمة في البنوك التشاركية، ومحاكاة تأثيرها على الأداء المالي وسرعة تعديل رأس المال. مناسبة للباحثين، الطلاب، والممارسين.")

# تبويبات رئيسية
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1️⃣ إدخال مؤشرات الحوكمة",
    "2️⃣ محاكاة تعديل رأس المال",
    "3️⃣ تحليل الأداء المالي",
    "4️⃣ تقييم جودة الحوكمة",
    "5️⃣ تحسين رأس المال",
    "6️⃣ تحسين العائد"
])

with tab1:
    st.subheader("1️⃣ إدخال مؤشرات الحوكمة")
    st.markdown("📝 في هذا القسم يمكنك إدخال درجات تقييم مكونات الحوكمة للبنك مثل الشفافية، الاستقلالية، والمخاطر. سيتم حساب مؤشر الحوكمة الكلي بناءً على هذه القيم لتُستخدم لاحقًا في التحليل والمحاكاة.")
    
    with st.expander("📘 ما هي منهجية حساب مؤشر الحوكمة؟"):
        st.markdown("""
        يتم حساب مؤشر الحوكمة الكلي بناءً على **متوسط مرجّح** لمجموعة من المؤشرات الفرعية:

        - 🔍 الشفافية والإفصاح (25%)
        - 👥 استقلالية مجلس الإدارة (25%)
        - 📊 فاعلية لجنة المراجعة (20%)
        - ⚠️ دور لجنة المخاطر (15%)
        - 🛡️ حماية حقوق المساهمين (15%)

        كل مؤشر يُقيَّم من 0 إلى 10، ويُحسب المؤشر النهائي كمتوسط مرجّح يعكس مستوى الحوكمة المؤسسية.
        """)

    transparency = st.number_input("الشفافية والإفصاح", min_value=0.0, max_value=10.0, value=6.0, step=0.1, format="%.1f")
    board_independence = st.number_input("استقلالية مجلس الإدارة", min_value=0.0, max_value=10.0, value=5.0, step=0.1, format="%.1f")
    audit_committee = st.number_input("فاعلية لجنة المراجعة", min_value=0.0, max_value=10.0, value=7.0, step=0.1, format="%.1f")
    risk_committee = st.number_input("دور لجنة المخاطر", min_value=0.0, max_value=10.0, value=4.0, step=0.1, format="%.1f")
    shareholder_rights = st.number_input("حماية حقوق المساهمين", min_value=0.0, max_value=10.0, value=6.0, step=0.1, format="%.1f")

    if st.button("حساب مؤشر الحوكمة"):
        weights = {
            "transparency": 0.25,
            "board": 0.25,
            "audit": 0.2,
            "risk": 0.15,
            "shareholders": 0.15
        }

        governance_metrics = {
            "transparency": transparency,
            "board": board_independence,
            "audit": audit_committee,
            "risk": risk_committee,
            "shareholders": shareholder_rights
        }

        governance_score = sum(governance_metrics[k] * weights[k] for k in governance_metrics)

        st.session_state["governance_score"] = governance_score

        st.success(f"✅ مؤشر الحوكمة الكلي: {governance_score:.2f} / 10")

        # رسم بياني توزيع الدرجات
        labels = ["الشفافية", "الاستقلالية", "المراجعة", "المخاطر", "حقوق المساهمين"]
        values = list(governance_metrics.values())

        # إنشاء DataFrame
        df_bar = pd.DataFrame({
            "المكون": labels,
            "الدرجة": values
        })

        # ربط كل مكون بلونه الخاص
        custom_colors = {
            "الشفافية": "#1f77b4",
            "الاستقلالية": "#2ca02c",
            "المراجعة": "#ff7f0e",
            "المخاطر": "#d62728",
            "حقوق المساهمين": "#9467bd"
        }

        # رسم العمود بدون تدرج لوني تلقائي
        fig_bar = px.bar(
            df_bar,
            x="المكون",
            y="الدرجة",
            title="توزيع درجات مؤشرات الحوكمة",
            color="المكون",  # التلوين حسب الفئة وليس القيمة
            color_discrete_map=custom_colors,
            range_y=[0, 10]
        )

        # إزالة الخلفية البيضاء وتنسيق الخط
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black', size=14),
            title_font=dict(size=18, color='black')
        )
        
        # عرض الرسم البياني
        st.plotly_chart(fig_bar)
        
        # حساب المساهمة النسبية (النسبة المئوية)
        percentages = {k: governance_metrics[k] * weights[k] * 10 for k in governance_metrics}

        labels_ar = {
            "transparency": "الشفافية",
            "board": "الاستقلالية",
            "audit": "المراجعة",
            "risk": "المخاطر",
            "shareholders": "حقوق المساهمين"
        }

        df_percent = pd.DataFrame({
            "المكون": [labels_ar[k] for k in percentages.keys()],
            "المساهمة في المؤشر الكلي (%)": list(percentages.values())
        })

        st.table(df_percent.style.format({"المساهمة في المؤشر الكلي (%)": "{:.2f}"}))

        # توصيات مفصلة
        st.markdown("###  توصيات تفصيلية:")
        if transparency < 5:
            st.markdown("- 🔍 تحسين الشفافية والإفصاح.")
        else:
            st.markdown("- ✅ الشفافية جيدة، يُنصح بالاستمرار في الإفصاح الفعّال.")
        if board_independence < 5:
            st.markdown("- 👥 تعزيز استقلالية مجلس الإدارة.")
        else:
            st.markdown("- ✅ استقلالية المجلس مقبولة، يُنصح بتعزيز الحوكمة الإستراتيجية.")
        if audit_committee < 5:
            st.markdown("- 📊 تحسين فاعلية لجنة المراجعة.")
        else:
            st.markdown("- ✅ لجنة المراجعة فعّالة، يُنصح بالحفاظ على دورها الرقابي.")
        if risk_committee < 5:
            st.markdown("- ⚠️ تفعيل دور لجنة المخاطر.")
        else:
            st.markdown("- ✅ لجنة المخاطر نشطة، مما يعزز مرونة البنك.")
        if shareholder_rights < 5:
            st.markdown("- 🛡️ ضمان حماية حقوق المساهمين.")
        else:
            st.markdown("- ✅ حقوق المساهمين محفوظة بشكل جيد، مما يعزز ثقة المستثمرين.")

        # نص تحليلي مفسر لنتيجة المؤشر
        st.markdown("---")
        st.markdown("#### 📌 تفسير عام لمؤشر الحوكمة الكلي:")
        if governance_score >= 8:
            st.success(
                "مؤشر الحوكمة مرتفع جدًا، مما يدل على هيكل حوكمة قوي وفعّال يدعم استقرار البنك وقدرته على مواجهة الصدمات."
            )
        elif governance_score >= 5:
            st.warning(
                "مؤشر الحوكمة متوسط، وهناك حاجة لتحسين بعض الجوانب لتعزيز الاستقرار والشفافية."
            )
        else:
            st.error(
                "مؤشر الحوكمة منخفض، وهذا يشير إلى مخاطر على استدامة البنك ويستلزم إجراءات تحسين فورية."
            )

with tab2:
    st.subheader("2️⃣ محاكاة تعديل رأس المال")
    st.markdown("📊 في هذا القسم يمكنك محاكاة مدى سرعة استجابة البنك لتعديل رأس ماله عند حدوث صدمة مالية. تعتمد النتيجة على مستوى الحوكمة ونوع الصدمة وقيمة رأس المال.")

    
    with st.expander("📘 كيف يتم حساب سرعة تعديل رأس المال؟"):
        st.markdown("""
        تستخدم المنصة هذه المعادلة لمحاكاة زمن تعديل رأس المال بعد الصدمة:

        $$
        \\text{المدة (بالأيام)} = \\frac{\\text{رأس المال} \\times \\text{معامل الصدمة}}{\\text{مؤشر الحوكمة} + 1}
        $$

        - 🏦 رأس المال يُدخل بالمليون.
        - ⚠️ نوع الصدمة يحدد معاملها:
            - انخفاض السيولة = 0.3
            - خسائر تشغيلية = 0.5
            - تشديد رقابي = 0.4
        - 📈 كلما ارتفع مؤشر الحوكمة، قلت المدة الزمنية.
        """)

    if "governance_score" not in st.session_state:
        st.error("⚠️ الرجاء إدخال مؤشرات الحوكمة أولاً في التبويب 1.")
    else:
        capital = st.number_input("رأس المال الحالي (بالدرهم)", min_value=0.00, value=100.0)
        shock_type = st.selectbox("نوع الصدمة", ["انخفاض في السيولة", "خسائر تشغيلية", "تشديد رقابي"])

        def simulate_adjustment(capital, governance_score, shock_type):
            impact = {"انخفاض في السيولة": 0.3, "خسائر تشغيلية": 0.5, "تشديد رقابي": 0.4}
            duration = (capital * impact[shock_type]) / (governance_score + 1)
            return round(duration, 2)

        if st.button("تنفيذ المحاكاة"):
            days = simulate_adjustment(capital, st.session_state["governance_score"], shock_type)
            st.success(f"⏱️ الزمن التقديري لتعديل رأس المال: **{days} يومًا**")

            if days <= 7:
                st.info("✅ استجابة سريعة تدل على حوكمة قوية ومرونة مالية.")
            elif days <= 14:
                st.warning("⚠️ استجابة متوسطة، ينصح بتحسين السيولة.")
            else:
                st.error("❗ استجابة بطيئة، قد تؤثر على الاستقرار المالي.")

            timeline = list(range(1, int(days) + 1))
            values = [capital - (i * capital * 0.025) for i in timeline]
            df_chart = pd.DataFrame({"يوم": timeline, "رأس المال المتوقع": values})
            st.line_chart(df_chart.set_index("يوم"))

            decrease_pct = round((capital - values[-1]) / capital * 100, 2)
            st.metric(label="النسبة المئوية للانخفاض في رأس المال", value=f"{decrease_pct}%")

            st.markdown("###  توصيات مخصصة:")
            if st.session_state["governance_score"] < 6:
                st.markdown("- 🔁 تحسين مؤشرات الحوكمة، خاصة الشفافية والمخاطر.")
            if shock_type == "خسائر تشغيلية":
                st.markdown("- ⚙️ تقوية أنظمة الرقابة التشغيلية.")
            if shock_type == "انخفاض في السيولة":
                st.markdown("- 💧 تحسين إدارة السيولة.")
            if shock_type == "تشديد رقابي":
                st.markdown("- 📚 مراجعة الالتزام التنظيمي.")

            # إضافة نص تحليلي مفسر
            st.markdown("---")
            st.markdown("#### 📌 تفسير نتيجة المحاكاة:")
            if days <= 7:
                st.success(
                    "مدة تعديل رأس المال القصيرة تعكس قدرة البنك على الاستجابة السريعة والتعامل مع الصدمات المالية بفعالية، "
                    "وهي علامة إيجابية تعكس قوة الحوكمة والسيولة."
                )
            elif days <= 14:
                st.warning(
                    "مدة تعديل رأس المال المتوسطة تشير إلى وجود بعض التحديات في سرعة التكيف مع الصدمات، "
                    "وينصح بمراجعة آليات إدارة السيولة وتحسين الحوكمة لتعزيز المرونة."
                )
            else:
                st.error(
                    "مدة تعديل رأس المال الطويلة تنبه إلى وجود مشاكل جوهرية في القدرة على الاستجابة، "
                    "مما قد يعرض البنك لمخاطر مالية كبيرة ويحتاج إلى إصلاحات عاجلة في الحوكمة وإدارة المخاطر."
                )

with tab3:
    st.subheader("3️⃣ تحليل الأداء المالي")

    st.markdown("📊 في هذا القسم يمكنك تحليل العلاقة بين مؤشرات الحوكمة والأداء المالي للبنك باستخدام معامل الارتباط بيرسون. يتم ذلك بناءً على الملف الذي تقوم بتحميله والذي يحتوي على مؤشرات مالية مثل ROA، ROE، وغيرها.")

    with st.expander("📘 كيف يتم تحليل العلاقة بين الحوكمة والأداء المالي؟"):
        st.markdown("""
        يتم استخدام معامل الارتباط بيرسون (Pearson Correlation) لقياس العلاقة بين `Governance_Score` وأحد المؤشرات المالية مثل ROA أو ROE:

        - 📌 خطوات التحليل:
            - تحميل البيانات المالية بصيغة CSV أو Excel
            - اختيار مؤشر مالي من القائمة
            - حساب معامل الارتباط وتحليل قوة العلاقة

        - 🧮 تفسير قيم معامل الارتباط:
            - ✅ بين 0.7 و 1.0: علاقة قوية جدًا
            - ⚠️ بين 0.4 و 0.7: علاقة متوسطة
            - 🔍 بين 0.2 و 0.4: علاقة ضعيفة
            - ❌ أقل من 0.2: لا توجد علاقة

        ⚠️ تأكد من تنوع البيانات للحصول على نتائج دقيقة وذات معنى.
        """)

    if "governance_score" not in st.session_state:
        st.error("⚠️ الرجاء إدخال مؤشرات الحوكمة أولاً في التبويب 1.")
    else:
        uploaded_file = st.file_uploader("📁 ارفع ملف الأداء المالي (CSV أو Excel)", type=["csv", "xlsx"])
        if uploaded_file:
            if uploaded_file.name.endswith("csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.dataframe(df.head())

            if "Governance_Score" not in df.columns:
                df["Governance_Score"] = st.session_state["governance_score"]
                st.info("✅ تم إضافة عمود مؤشر الحوكمة تلقائيًا.")

            num_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
            if "Governance_Score" in num_cols:
                num_cols.remove("Governance_Score")

            if num_cols:
                selected_metric = st.selectbox("📈 اختر مؤشرًا ماليًا للتحليل", num_cols)

                df_clean = df[["Governance_Score", selected_metric]].copy()
                df_clean["Governance_Score"] = pd.to_numeric(df_clean["Governance_Score"], errors="coerce")
                df_clean[selected_metric] = pd.to_numeric(df_clean[selected_metric], errors="coerce")
                df_clean = df_clean.dropna()

                if df_clean["Governance_Score"].nunique() <= 1 or df_clean[selected_metric].nunique() <= 1:
                    st.warning("⚠️ البيانات لا تحتوي على تباين كافٍ لحساب معامل الارتباط.")
                else:
                    corr = df_clean["Governance_Score"].corr(df_clean[selected_metric])
                    st.metric(label="📊 معامل الارتباط", value=f"{corr:.2f}")

                    fig = px.scatter(df_clean, x="Governance_Score", y=selected_metric,
                                     trendline="ols",
                                     title=f"العلاقة بين الحوكمة و {selected_metric}",
                                     labels={"Governance_Score": "مؤشر الحوكمة", selected_metric: selected_metric})
                    st.plotly_chart(fig)

                    # تحليل العلاقة بناءً على القيمة
                    if corr >= 0.7:
                        st.success("✅ علاقة قوية جدًا بين الحوكمة والمؤشر المالي.")
                    elif corr >= 0.4:
                        st.info("ℹ️ علاقة معتدلة، تحتاج مراقبة وتحسين.")
                    elif corr >= 0.2:
                        st.warning("⚠️ علاقة ضعيفة نسبيًا، ينصح بالتحقق من البيانات.")
                    else:
                        st.error("❗ لا توجد علاقة واضحة.")

                    # تفسير تفصيلي
                    st.markdown("---")
                    st.markdown("#### 📌 تفسير تفصيلي لنتيجة معامل الارتباط:")

                    if corr >= 0.7:
                        st.success(
                            "العلاقة القوية بين الحوكمة والأداء المالي تعني أن البنك الذي يتمتع بهياكل حوكمة قوية "
                            "يحقق عادة أداء مالي أفضل. هذا يعود إلى كفاءة اتخاذ القرار، تقليل المخاطر، وثقة المستثمرين."
                        )
                    elif corr >= 0.4:
                        st.info(
                            "العلاقة المتوسطة تشير إلى تأثير ملحوظ ولكن غير حاسم. من الأفضل التحقق من جودة البيانات وتحليل العوامل الخارجية."
                        )
                    elif corr >= 0.2:
                        st.warning(
                            "العلاقة الضعيفة قد تعكس نقصًا في تنوع البيانات أو عوامل خفية تؤثر على الأداء."
                        )
                    else:
                        st.error(
                            "عدم وجود علاقة واضحة يشير إلى ضعف انعكاس الحوكمة على الأداء المالي. يفضل مراجعة الاستراتيجية والبيانات."
                        )
                    # تحليل الانحدار الخطي وتقييم النموذج
                    if abs(corr) >= 0.4:
                        X = df_clean[["Governance_Score"]].values
                        y = df_clean[selected_metric].values

                        model = LinearRegression()
                        model.fit(X, y)
                        y_pred = model.predict(X)

                        r2 = model.score(X, y)
                        mae = mean_absolute_error(y, y_pred)
                        mse = mean_squared_error(y, y_pred)
                        rmse = mse ** 0.5

                        st.markdown("### 🔍 نتائج تحليل الانحدار:")
                        st.metric("📊 معامل التحديد R²", f"{r2:.3f}")
                        st.metric("📉 متوسط الخطأ المطلق (MAE)", f"{mae:.3f}")
                        st.metric("📉 متوسط مربع الخطأ (MSE)", f"{mse:.3f}")
                        st.metric("📉 الجذر التربيعي لمتوسط الخطأ (RMSE)", f"{rmse:.3f}")

                        st.markdown("---")
                        st.markdown(f"#### 📌 معادلة الانحدار:")
                        st.markdown(f"""
                        <div style='background-color:#f0f2f6; padding:15px; border-radius:10px; font-size:18px;'>
                        💡 <b>{selected_metric} = {model.coef_[0]:.3f} × مؤشر الحوكمة + {model.intercept_:.3f}</b><br><br>
                        🧮 هذا يعني أنه لكل وحدة زيادة في مؤشر الحوكمة، يرتفع <b>{selected_metric}</b> بمقدار <b>{model.coef_[0]:.3f}</b> نقطة تقريبًا.<br>
                        📉 عندما يكون مؤشر الحوكمة = 0، فإن القيمة التقديرية لـ <b>{selected_metric}</b> تساوي <b>{model.intercept_:.3f}</b>.<br>
                        📊 على سبيل المثال، إذا كانت درجة الحوكمة = 7، فإن:<br>
                        <b>{selected_metric} = {model.coef_[0]:.3f} × 7 + {model.intercept_:.3f} = {(model.coef_[0] * 7 + model.intercept_):.3f}</b>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("### تفسير النموذج:")
                        if r2 >= 0.7:
                            st.success("النموذج يفسر نسبة كبيرة من التغير في الأداء المالي استنادًا إلى الحوكمة. موثوق جدًا.")
                        elif r2 >= 0.4:
                            st.info("النموذج يفسر جزءًا معقولًا من التغيرات. مفيد لكن يحتاج دعم بمتغيرات إضافية.")
                        else:
                            st.warning("النموذج ضعيف في تفسير العلاقة. قد تكون العلاقة غير خطية أو هناك متغيرات مؤثرة أخرى.")
with tab4:
    st.subheader("4️⃣ تقييم جودة الحوكمة")

    with st.expander("📘 كيف يتم تقييم الحوكمة من الملفات؟"):
        st.markdown("""
        عند رفع ملف Excel أو CSV يحتوي على مؤشرات الحوكمة التالية:

        - Transparency
        - Board_Independence
        - Audit_Committee
        - Risk_Committee
        - Shareholder_Rights

        تقوم المنصة بحساب مؤشر الحوكمة لكل مؤسسة أو حسب السنوات لنفس المؤسسة بنفس الطريقة المستخدمة في التبويب الأول (متوسط مرجّح).
        ثم يتم تحليل:
        - ✅ المتوسط العام
        - 📊 توزيع الدرجات عبر المؤسسات
        - 🧠 توصيات بناءً على الأداء العام للحوكمة في القطاع.
        """)

    uploaded_file = st.file_uploader("📁 ارفع ملف تقييم (Excel أو CSV)", type=["xlsx", "csv"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        st.dataframe(df)

        required_cols = ["Transparency", "Board_Independence", "Audit_Committee", "Risk_Committee", "Shareholder_Rights"]
        if all(col in df.columns for col in required_cols):
            weights = [0.25, 0.25, 0.2, 0.15, 0.15]
            df["Governance_Score"] = df[required_cols].dot(weights)
            st.success("✅ تم احتساب مؤشر الحوكمة")
            st.dataframe(df[["Governance_Score"]])

            avg_score = df["Governance_Score"].mean()
            if avg_score >= 8:
                st.info(f"🏆 متوسط الحوكمة عالي ({avg_score:.2f})، الأداء جيد.")
            elif avg_score >= 5:
                st.warning(f"⚠️ متوسط الحوكمة متوسط ({avg_score:.2f})، تفاوت بين المؤسسات.")
            else:
                st.error(f"❗ متوسط الحوكمة ضعيف ({avg_score:.2f})، حاجة لتحسين.")

            st.markdown("###  توصيات:")
            if avg_score < 5:
                st.markdown("- 🛠️  تحسين شامل للحوكمة عبر المؤسسات او السنوات.")
            elif avg_score < 8:
                st.markdown("- 🧩 مشاركة أفضل الممارسات بين المؤسسات او السنوات.")
            else:
                st.markdown("- ✅ الاستمرار في التحسينات الحالية.")

            fig2 = px.histogram(df, x="Governance_Score", title="توزيع درجات الحوكمة")
            st.plotly_chart(fig2)

            # شرح مفسر لنتيجة متوسط الحوكمة
            st.markdown("---")
            st.markdown("#### 📌 تفسير متوسط مؤشر الحوكمة:")
            if avg_score >= 8:
                st.success(
                    "متوسط الحوكمة العالي يدل على أن المؤسسة أو المؤسسات بشكل عام تحكم جيد ومستقر، وهذا يشير إلى "
                    "بيئة أعمال سليمة وتحكم فعال."
                )
            elif avg_score >= 5:
                st.warning(
                    "متوسط الحوكمة المتوسط يعكس تفاوتًا في جودة الحوكمة ، وينصح بتبادل الخبرات "
                    "وتبني ممارسات أفضل."
                )
            else:
                st.error(
                    "متوسط الحوكمة المنخفض يشير إلى وجود مشاكل كبيرة في الحوكمة على مستوى عدد السنوات أو المؤسسات، "
                    "مما يستدعي تدخلات إصلاحية عاجلة."
                )
        else:
            st.warning("⚠️ تأكد من وجود الأعمدة المطلوبة في الملف.")

# تبويب 5: تحسين رأس المال بعد الصدمة
with tab5:
    st.subheader("5️⃣ تحسين رأس المال بعد الصدمة - بقيود")

    st.markdown("📝 في هذا القسم يتم تحسين توزيع رأس المال بعد تعرض البنك لصدمة، مع مراعاة مستويات الحوكمة والقيود التنظيمية.")
    
    with st.expander("📘 ما هي منهجية حساب زمن تعديل رأس المال؟"):
        st.markdown("""
        يتم حساب زمن تعديل رأس المال بعد الصدمة بناءً على **تقييم مستوى الحوكمة لكل وحدة** والحد الأدنى المؤهل للمشاركة في التحسين:

        - ✅ فقط الوحدات التي تحقق حد الحوكمة الأدنى تُعتبر مؤهلة.
        - ⏱️ زمن التعديل يُحسب كنسبة بين رأس المال المخصص للكل وحدة وتأثير الصدمة مضروبًا بعامل يعكس مستوى الحوكمة.
        - 💡 كلما ارتفع مستوى الحوكمة، كلما قل زمن تعديل رأس المال، مما يعكس مرونة واستجابة أسرع.
        - 🛑 يتم فرض قيود على الحد الأقصى لرأس المال لكل وحدة لضمان الالتزام التنظيمي.

        هذه المنهجية تتيح توزيعًا متوازنًا ومرنًا لرأس المال لتحسين سرعة التكيف مع الصدمات المالية.
        """)

    num_units = st.number_input("🔢 عدد الوحدات", 2, 10, 3)
    total_capital = st.number_input("💰 رأس المال (مليون)", 0.0, 10000.0, 100.0)
    shock_impact = st.number_input("⚠️ معامل الصدمة", 0.1, 1.0, 0.3)
    min_gov = st.number_input("📉 الحد الأدنى للحوكمة", 0.0, 10.0, 5.0)
    max_alloc = st.number_input("🔒 الحد الأقصى للوحدة (مليون)", 0.0)

    g_arr = [st.number_input(f"حوكمة وحدة {i+1}", 0.0, 10.0, 6.0) for i in range(int(num_units))]

    if st.button("🔄 تحسين التوزيع"):
        g_arr = np.array(g_arr)
        eff = g_arr + 1
        eligible = g_arr >= min_gov
        eff[~eligible] = 0

        weights = eff / eff.sum() if eff.sum() > 0 else np.zeros_like(eff)
        alloc = weights * total_capital
        alloc = np.minimum(alloc, max_alloc)

        unused = total_capital - alloc.sum()
        room = max_alloc - alloc
        if room.sum() > 0 and unused > 0:
            share = room / room.sum()
            alloc += unused * share

        duration = (alloc * shock_impact) / (g_arr + 1)

        df_alloc = pd.DataFrame({
            "الوحدة": [f"وحدة {i+1}" for i in range(num_units)],
            "مؤهل؟": ["✅" if e else "❌" for e in eligible],
            "مستوى الحوكمة": g_arr,
            "رأس المال المخصص": alloc,
            "زمن التعديل (يوم)": duration
        })

        st.dataframe(df_alloc.style.format({"رأس المال المخصص": "{:.2f}", "زمن التعديل (يوم)": "{:.2f}"}))
        st.metric("⏱️ الزمن الكلي", f"{duration.sum():.2f} يومًا")

        fig = px.bar(df_alloc, x="الوحدة", y="رأس المال المخصص", color="مؤهل؟", text="زمن التعديل (يوم)")
        st.plotly_chart(fig)

        # --- تحليل الحساسية ---
        shock_values = np.linspace(0.1, 1.0, 10)
        avg_durations = []
        for val in shock_values:
            dur = (alloc * val) / (g_arr + 1)
            avg_durations.append(dur.mean())

        fig_sensitivity = px.line(
            x=shock_values, y=avg_durations,
            labels={"x": "معامل الصدمة", "y": "متوسط زمن التعديل (يوم)"},
            title="تحليل حساسية متوسط زمن التعديل لمعان الصدمة"
        )
        st.plotly_chart(fig_sensitivity)

        # --- تحليلات إضافية ---
        st.markdown("---")
        st.subheader("📊 تحليلات وتفسيرات ذكية:")

        num_eligible = eligible.sum()
        percent_eligible = num_eligible / num_units * 100
        st.markdown(f"✅ **عدد الوحدات المؤهلة:** {num_eligible} من {num_units} وحدة ({percent_eligible:.1f}%)")

        slowest_unit = df_alloc.loc[df_alloc["زمن التعديل (يوم)"].idxmax()]
        st.markdown(f"🐢 **أبطأ وحدة في التعديل:** {slowest_unit['الوحدة']} (حوكمة: {slowest_unit['مستوى الحوكمة']}, زمن: {slowest_unit['زمن التعديل (يوم)']:.2f} يوم)")

        over_25 = (df_alloc["رأس المال المخصص"] > total_capital * 0.25).sum()
        if over_25:
            st.warning(f"⚠️ يوجد {over_25} وحدة تستحوذ على أكثر من 25% من رأس المال، مما قد يشير إلى تركّز مالي غير متوازن.")

        # --- توصيات مخصصة ---
        st.markdown("### 🤖 توصيات تلقائية:")
        if percent_eligible < 50:
            st.error("- 🔁 نسبة الوحدات المؤهلة منخفضة. يوصى بتحسين مستويات الحوكمة بشكل عام.")
        elif percent_eligible < 80:
            st.warning("- ⚠️ نسبة متوسطة من الوحدات مؤهلة. يمكن تحسين بعض الجوانب في الحوكمة لتوسيع المشاركة.")
        else:
            st.success("- ✅ نسبة ممتازة من الوحدات مؤهلة. التوزيع مرن ويعكس جاهزية عالية.")

        if slowest_unit['زمن التعديل (يوم)'] > 20:
            st.error("- ⏳ هناك وحدة تستغرق وقتًا طويلاً في تعديل رأس المال. راجع مؤشرات الحوكمة الخاصة بها.")
        elif slowest_unit['زمن التعديل (يوم)'] > 10:
            st.warning("- 🐌 وحدة واحدة على الأقل بطيئة نسبيًا. تحسين حوكمتها يعزز سرعة الاستجابة.")
        else:
            st.success("- 🚀 جميع الوحدات لديها زمن تعديل مقبول.")


# تبويب 6: تحسين العائد باستخدام لاكرانج + مؤشرات المخاطر + نموذج تحسين متعدد
with tab6:
    st.subheader("6️⃣ تحسين العائد باستخدام مضاعفات لاكرانج")

    st.markdown("📝 في هذا القسم يتم تحسين توزيع الاستثمارات لتحقيق أعلى عائد ممكن ضمن قيود المخاطر والحدود التنظيمية.")

    total_capital = st.number_input("💰 القيمة الإجمالية المتاحة للاستثمار (بالدرهم)", min_value=1.0, value=3_000_000.0)

    with st.expander("📘 ما هي منهجية تحسين العائد مقابل المخاطرة؟"):
        st.markdown("""
        يتم تحسين توزيع الاستثمارات عبر محفظة مالية باستخدام **مضاعفات لاكرانج** لتحقيق توازن بين:

        - 📈 زيادة العائد المتوقع للمحفظة.
        - ⚖️ تقليل المخاطر (المقاسة بالانحراف المعياري أو التغاير).
        - 🔒 احترام القيود المفروضة على الحد الأدنى والأقصى لكل استثمار.
        - 🎯 استخدام نموذج رياضي يعتمد على دالة الهدف التي توازن بين العائد والمخاطر.
        - 🤖 تحليل الحساسية لفهم تأثير تغير العوائد على المحفظة.

        هذه المنهجية تتيح اختيار أفضل توزيع للأصول لتحقيق أفضل أداء مالي ممكن ضمن قيود المخاطر والتنظيم.
        """)

    n_assets = st.number_input("🔢 عدد الاستثمارات", 2, 10, 3)
    r_list, max_list, min_list = [], [], []

    for i in range(int(n_assets)):
        r = st.number_input(f"📈 عائد الاستثمار {i+1} (%)", key=f"r{i}")
        max_dh = st.number_input(f"🔒 الحد الأقصى للاستثمار {i+1} (بالدرهم)", min_value=0.0, value=1_000_000.0, key=f"max{i}")
        min_dh = st.number_input(f"⬇️ الحد الأدنى للاستثمار {i+1} (بالدرهم)", min_value=0.0, value=100_000.0, key=f"min{i}")
        
        r_list.append(r / 100)
        max_list.append(max_dh / total_capital)  # تحويل القيمة إلى نسبة (وزن)
        min_list.append(min_dh / total_capital)

    cov_matrix = np.identity(int(n_assets)) * 0.02  # مصفوفة التغاير (بسيطة مؤقتًا)

    if st.button("🚀 تنفيذ تحسين العائد"):
        r = np.array(r_list)
        max_c = np.array(max_list)
        min_c = np.array(min_list)

        base = r / r.sum()
        w = np.maximum(base, min_c)
        w = np.minimum(w, max_c)

        unused = 1.0 - w.sum()
        if unused > 0:
            room = max_c - w
            room[room < 0] = 0
            share = room / room.sum()
            w += unused * share

        if w.sum() > 1:
            w = w / w.sum()

        p_return = np.dot(w, r)
        port_variance = np.dot(w.T, np.dot(cov_matrix, w))
        port_std = np.sqrt(port_variance)

        risk_free_rate = 0.02
        sharpe_ratio = (p_return - risk_free_rate) / port_std if port_std != 0 else 0

        sensitivity = []
        delta = 0.01
        for i in range(len(r)):
            r_sens = r.copy()
            r_sens[i] += delta
            p_return_sens = np.dot(w, r_sens)
            sensitivity.append((p_return_sens - p_return) / delta)

        equal_w = np.ones_like(w) / len(w)
        equal_return = np.dot(equal_w, r)

        unconstrained_w = base / base.sum()
        unconstrained_return = np.dot(unconstrained_w, r)

        df_result = pd.DataFrame({
            "الاستثمار": [f"استثمار {i+1}" for i in range(n_assets)],
            "الوزن الأمثل": w,
            "العائد المتوقع (%)": r * 100,
            "المساهمة في العائد (%)": w * r * 100,
            "الحد الأقصى (درهم)": np.array(max_list) * total_capital,
            "الحد الأدنى (درهم)": np.array(min_list) * total_capital,
            "حساسية العائد": sensitivity
        })

        st.dataframe(df_result.style.format({
            "الوزن الأمثل": "{:.2%}",
            "المساهمة في العائد (%)": "{:.2f}",
            "الحد الأقصى (درهم)": "{:,.0f}",
            "الحد الأدنى (درهم)": "{:,.0f}",
            "حساسية العائد": "{:.4f}"
        }))

        st.metric("📊 العائد الكلي المتوقع", f"{p_return*100:.2f}%")
        st.metric("⚖️ العائد مع توزيع متساوي", f"{equal_return*100:.2f}%")
        st.metric("📉 الانحراف المعياري (مخاطر المحفظة)", f"{port_std*100:.2f}%")
        st.metric("📈 مؤشر شارب (Sharpe Ratio)", f"{sharpe_ratio:.2f}")

        st.write(f"📌 العائد بدون قيود: {unconstrained_return*100:.2f}%")
        st.write(f"📌 الفرق بسبب القيود: {(unconstrained_return - p_return)*100:.2f}%")

        fig = px.bar(df_result, x="الاستثمار", y="الوزن الأمثل", color="العائد المتوقع (%)",
                     labels={"الوزن الأمثل": "الوزن الأمثل (%)", "العائد المتوقع (%)": "العائد المتوقع (%)"})
        st.plotly_chart(fig)

        # --- نموذج تحسين باستخدام CVXPY ---
        st.subheader("تحسين العائد مقابل المخاطرة باستخدام CVXPY")

        n = len(r_list)
        w_var = cp.Variable(n)
        r_arr = np.array(r_list)
        cov = np.diag(np.full(n, 0.02))  # تغاير ثابت افتراضي

        _lambda = 0.1  # عامل الخطر

        objective = cp.Maximize(r_arr.T @ w_var - _lambda * cp.quad_form(w_var, cov))
        constraints = [cp.sum(w_var) == 1,
                       w_var >= np.array(min_list),
                       w_var <= np.array(max_list)]
        prob = cp.Problem(objective, constraints)
        prob.solve()

        optimal_weights = w_var.value

        df_opt = pd.DataFrame({
            "الاستثمار": [f"استثمار {i+1}" for i in range(n)],
            "الوزن الأمثل (CVXPY)": optimal_weights
        })
        st.dataframe(df_opt.style.format({"الوزن الأمثل (CVXPY)": "{:.2%}"}))

        st.markdown("### 🤖 توصيات:")
        if sharpe_ratio < 1:
            st.warning("مخاطر المحفظة عالية نسبيًا، يُنصح بإعادة توزيع الأوزان أو زيادة التنويع.")
        else:
            st.success("المحفظة متوازنة جيدًا مع عائد ومخاطر محسوبة.")

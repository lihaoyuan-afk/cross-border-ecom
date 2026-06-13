"""
Amazon 选品分析工具 - Streamlit 主应用
启动：streamlit run app.py
"""

import os
import re
from collections import Counter

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ── 页面配置 ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Amazon 选品分析工具",
    page_icon="📦",
    layout="wide",
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "amazon_products.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    df["listed_date"] = pd.to_datetime(df["listed_date"])
    return df


def score_badge(score: float) -> str:
    if score >= 80:
        return "🟢"
    if score >= 60:
        return "🟡"
    return "🔴"


# ── 数据加载 ─────────────────────────────────────────────────
if not os.path.exists(DATA_PATH):
    st.error("未找到数据文件，请先运行 `python generate_data.py`")
    st.stop()

df = load_data()

# ── 全局侧边栏筛选 ────────────────────────────────────────────
with st.sidebar:
    st.title("📦 选品分析工具")
    st.caption("Amazon 跨境电商选品辅助决策系统")
    st.divider()

    selected_cats = st.multiselect(
        "类目筛选",
        options=df["category"].unique().tolist(),
        default=df["category"].unique().tolist(),
    )

    price_min, price_max = float(df["price"].min()), float(df["price"].max())
    price_range = st.slider(
        "价格区间 ($)",
        min_value=price_min,
        max_value=price_max,
        value=(price_min, price_max),
        step=1.0,
    )

    min_rating = st.slider("最低评分", 1.0, 5.0, 3.5, step=0.1)
    max_bsr    = st.number_input("BSR 上限", min_value=1, max_value=30000, value=20000, step=1000)

    st.divider()
    st.caption("数据为模拟数据，仅供演示")

# 应用筛选条件
mask = (
    df["category"].isin(selected_cats) &
    df["price"].between(*price_range) &
    (df["rating"] >= min_rating) &
    (df["bsr"] <= max_bsr)
)
filtered = df[mask].copy()

st.info(f"当前筛选结果：**{len(filtered)}** 个商品（共 {len(df)} 个）", icon="🔍")

# ── 四个标签页 ────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 市场概览", "🏆 选品评分", "🔑 关键词分析", "⚔️ 竞争度分析"])


# ═══════════════════════════════════════════════════════════════
# TAB 1 — 市场概览
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.subheader("市场概览")

    if filtered.empty:
        st.warning("当前筛选条件下无数据")
    else:
        # KPI 卡片
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("商品总数",      f"{len(filtered)}")
        c2.metric("平均价格",      f"${filtered['price'].mean():.2f}")
        c3.metric("平均 BSR",      f"{filtered['bsr'].mean():,.0f}")
        c4.metric("平均月销售额",  f"${filtered['monthly_revenue'].mean():,.0f}")
        c5.metric("平均评分",      f"{filtered['rating'].mean():.2f}")

        st.divider()
        col_l, col_r = st.columns(2)

        with col_l:
            # 各类目商品数量
            cat_count = filtered["category"].value_counts().reset_index()
            cat_count.columns = ["类目", "商品数"]
            fig = px.bar(
                cat_count, x="类目", y="商品数",
                title="各类目商品数量",
                color="类目",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            # 各类目平均月销售额
            rev_by_cat = filtered.groupby("category")["monthly_revenue"].mean().reset_index()
            rev_by_cat.columns = ["类目", "平均月销售额($)"]
            fig2 = px.bar(
                rev_by_cat, x="类目", y="平均月销售额($)",
                title="各类目平均月销售额",
                color="类目",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

        col_l2, col_r2 = st.columns(2)

        with col_l2:
            # 价格分布直方图
            fig3 = px.histogram(
                filtered, x="price", nbins=20,
                title="价格分布",
                color_discrete_sequence=["#636EFA"],
                labels={"price": "价格 ($)", "count": "商品数"},
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col_r2:
            # 评分分布
            fig4 = px.histogram(
                filtered, x="rating", nbins=15,
                title="评分分布",
                color_discrete_sequence=["#EF553B"],
                labels={"rating": "评分", "count": "商品数"},
            )
            st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 — 选品评分
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.subheader("选品综合评分")
    st.caption(
        "评分权重：BSR 排名 40% · 评价数 20% · 评分 20% · 月销售额 10% · 价格合理性 10%"
    )

    if filtered.empty:
        st.warning("当前筛选条件下无数据")
    else:
        top_n = st.slider("展示 Top N 商品", 5, 50, 20)

        top_df = (
            filtered.sort_values("score", ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        top_df.index += 1

        # 评分条形图
        fig = px.bar(
            top_df, x="score", y="title",
            orientation="h",
            color="score",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            labels={"score": "综合评分", "title": "商品"},
            title=f"Top {top_n} 选品评分",
            hover_data=["brand", "category", "price", "bsr", "reviews", "monthly_revenue"],
        )
        fig.update_layout(yaxis={"autorange": "reversed"}, height=max(400, top_n * 28))
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        # 详情表格
        display_cols = {
            "score": "评分",
            "category": "类目",
            "brand": "品牌",
            "price": "价格($)",
            "bsr": "BSR",
            "rating": "评分",
            "reviews": "评价数",
            "monthly_revenue": "月销售额($)",
            "title": "商品标题",
        }
        show_df = top_df[list(display_cols)].rename(columns=display_cols)
        show_df["评分"] = show_df["评分"].apply(lambda s: f"{score_badge(s)} {s:.1f}")
        st.dataframe(show_df, use_container_width=True)

        st.divider()

        # 散点图：BSR vs 月销售额（气泡大小=评价数）
        st.subheader("BSR × 月销售额分布")
        fig2 = px.scatter(
            filtered,
            x="bsr", y="monthly_revenue",
            size="reviews",
            color="category",
            hover_data=["brand", "price", "rating", "score"],
            labels={"bsr": "BSR 排名", "monthly_revenue": "月销售额($)", "reviews": "评价数"},
            title="BSR 排名 vs 月销售额（气泡大小 = 评价数）",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3 — 关键词分析
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.subheader("标题关键词分析")

    if filtered.empty:
        st.warning("当前筛选条件下无数据")
    else:
        STOP_WORDS = {
            "with", "for", "and", "the", "in", "of", "to", "a", "an",
            "or", "on", "at", "by", "is", "are", "it", "its", "be",
            "as", "up", "-", "&",
        }

        all_words: list[str] = []
        for title in filtered["title"]:
            tokens = re.findall(r"[a-zA-Z]{2,}", title.lower())
            all_words.extend(w for w in tokens if w not in STOP_WORDS)

        word_freq = Counter(all_words)
        top_words = word_freq.most_common(30)

        col_l, col_r = st.columns([3, 2])

        with col_l:
            wf_df = pd.DataFrame(top_words, columns=["关键词", "出现次数"])
            fig = px.bar(
                wf_df, x="出现次数", y="关键词",
                orientation="h",
                color="出现次数",
                color_continuous_scale="Blues",
                title="Top 30 高频关键词",
            )
            fig.update_layout(yaxis={"autorange": "reversed"}, height=550)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("**Top 30 关键词频次表**")
            st.dataframe(
                wf_df.style.background_gradient(cmap="Blues", subset=["出现次数"]),
                use_container_width=True,
                height=540,
            )

        st.divider()

        # 各类目独立词频对比
        st.subheader("各类目高频关键词对比")
        cat_select = st.selectbox("选择类目", options=filtered["category"].unique().tolist())
        cat_df = filtered[filtered["category"] == cat_select]

        cat_words: list[str] = []
        for title in cat_df["title"]:
            tokens = re.findall(r"[a-zA-Z]{2,}", title.lower())
            cat_words.extend(w for w in tokens if w not in STOP_WORDS)

        cat_freq = pd.DataFrame(
            Counter(cat_words).most_common(15),
            columns=["关键词", "出现次数"],
        )
        fig2 = px.bar(
            cat_freq, x="关键词", y="出现次数",
            title=f"「{cat_select}」类目 Top 15 关键词",
            color="出现次数",
            color_continuous_scale="Greens",
        )
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 4 — 竞争度分析
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.subheader("市场竞争度分析")

    if filtered.empty:
        st.warning("当前筛选条件下无数据")
    else:
        # 竞争度指标：平均评价数越高、BSR 越低 → 竞争越激烈
        comp = (
            filtered.groupby("category")
            .agg(
                商品数=("asin", "count"),
                平均BSR=("bsr", "mean"),
                平均评价数=("reviews", "mean"),
                评价数中位数=("reviews", "median"),
                平均评分=("rating", "mean"),
                平均月销售额=("monthly_revenue", "mean"),
                平均选品评分=("score", "mean"),
            )
            .reset_index()
        )
        comp.columns.name = None
        comp = comp.rename(columns={"category": "类目"})

        # 竞争度综合指数（评价数多+BSR低 = 竞争激烈）
        comp["竞争指数"] = (
            (comp["平均评价数"] / comp["平均评价数"].max() * 50) +
            ((1 - comp["平均BSR"] / comp["平均BSR"].max()) * 50)
        ).round(1)

        # 雷达图：四类目多维度对比
        categories_radar = ["平均选品评分", "平均月销售额", "平均评分"]
        fig = go.Figure()

        colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]
        for i, row in comp.iterrows():
            norm_score = row["平均选品评分"] / 100
            norm_revenue = min(row["平均月销售额"] / 10000, 1.0)
            norm_rating = (row["平均评分"] - 1) / 4
            r_vals = [norm_score, norm_revenue, norm_rating, norm_score]
            theta_vals = ["选品潜力", "月销售额", "产品评分", "选品潜力"]

            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=theta_vals,
                fill="toself",
                name=row["类目"],
                line_color=colors[i % len(colors)],
                opacity=0.6,
            ))

        fig.update_layout(
            polar={"radialaxis": {"visible": True, "range": [0, 1]}},
            title="各类目综合对比雷达图（归一化）",
            height=450,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        col_l, col_r = st.columns(2)

        with col_l:
            # 竞争指数条形图
            fig2 = px.bar(
                comp.sort_values("竞争指数", ascending=True),
                x="竞争指数", y="类目",
                orientation="h",
                color="竞争指数",
                color_continuous_scale="RdYlGn_r",
                title="各类目竞争指数（越高越激烈）",
                range_color=[0, 100],
            )
            fig2.update_coloraxes(showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

        with col_r:
            # 平均评价数 vs 平均月销售额（机会象限）
            fig3 = px.scatter(
                comp,
                x="平均评价数", y="平均月销售额",
                size="商品数",
                color="类目",
                text="类目",
                title="机会象限：评价门槛 vs 市场规模",
                labels={"平均评价数": "进入门槛（平均评价数）", "平均月销售额": "市场规模（平均月销售额$）"},
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            fig3.update_traces(textposition="top center")

            # 添加象限参考线
            x_mid = comp["平均评价数"].median()
            y_mid = comp["平均月销售额"].median()
            fig3.add_hline(y=y_mid, line_dash="dot", line_color="gray", opacity=0.5)
            fig3.add_vline(x=x_mid, line_dash="dot", line_color="gray", opacity=0.5)

            # 象限标注
            fig3.add_annotation(text="⭐ 理想机会", x=comp["平均评价数"].min(), y=comp["平均月销售额"].max(),
                                showarrow=False, font_color="#00CC96", font_size=11)
            fig3.add_annotation(text="⚠️ 高门槛高回报", x=comp["平均评价数"].max(), y=comp["平均月销售额"].max(),
                                showarrow=False, font_color="#EF553B", font_size=11)

            st.plotly_chart(fig3, use_container_width=True)

        # 汇总数据表
        st.subheader("类目数据汇总")
        display_comp = comp.copy()
        display_comp["平均BSR"] = display_comp["平均BSR"].apply(lambda x: f"{x:,.0f}")
        display_comp["平均评价数"] = display_comp["平均评价数"].apply(lambda x: f"{x:,.0f}")
        display_comp["评价数中位数"] = display_comp["评价数中位数"].apply(lambda x: f"{x:,.0f}")
        display_comp["平均月销售额"] = display_comp["平均月销售额"].apply(lambda x: f"${x:,.0f}")
        display_comp["平均评分"] = display_comp["平均评分"].apply(lambda x: f"{x:.2f}")
        display_comp["平均选品评分"] = display_comp["平均选品评分"].apply(lambda x: f"{x:.1f}")
        st.dataframe(display_comp.set_index("类目"), use_container_width=True)

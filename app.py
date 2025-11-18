import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set page config
st.set_page_config(page_title="CPI Monte Carlo Simulator", layout="wide", initial_sidebar_state="expanded")

# Title
st.title("🎓 CPI Monte Carlo Simulator - B.Tech ECE")
st.markdown("---")

# Course structure with credits for each semester
course_structure = {
    1: [4, 4.5, 5.5, 2.5, 4.5, 2.5],
    2: [4, 4.5, 5.5, 1.5, 4, 3],
    3: [4, 3, 4, 4, 4, 3],
    4: [4, 3, 4, 3, 3, 3],
    5: [4, 4, 4, 3, 3, 3],
    6: [4, 4, 3, 3, 3, 3],
    7: [3, 3, 3, 3, 3, 6],
    8: [3, 3, 3, 8]
}

total_credits = sum(sum(credits) for credits in course_structure.values())

# Sidebar inputs
st.sidebar.header("📊 Input Parameters")

# Grade mapping
grade_mapping = {
    "AA": 10,
    "AB": 9,
    "BB": 8,
    "BC": 7,
    "CC": 6,
    "CD": 5,
    "DD": 4,
    "FF": 0
}

col1, col2 = st.sidebar.columns(2)
with col1:
    current_cpi = st.number_input("Current CPI", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
    lowest_grade_letter = st.selectbox("Lowest Grade of Last Semester", options=list(grade_mapping.keys()), index=2)

with col2:
    current_sem = st.number_input("Last Semester", min_value=1, max_value=7, value=1, step=1)
    highest_grade_letter = st.selectbox("Highest Grade of Last Semester", options=list(grade_mapping.keys()), index=1)

# Convert letter grades to numeric
lowest_grade = grade_mapping[lowest_grade_letter]
highest_grade = grade_mapping[highest_grade_letter]

num_simulations = st.sidebar.slider("Number of Simulations", min_value=100, max_value=10000, value=1000, step=100)

# Start button
st.sidebar.markdown("---")
start_button = st.sidebar.button("🚀 Start Simulation", use_container_width=True, type="primary")

if not start_button:
    st.info("👈 Click the **Start Simulation** button to begin!")
    st.stop()

# Validation checks
if current_sem is None:
    st.sidebar.error("❌ Please select a semester!")
    st.stop()
if lowest_grade > highest_grade:
    st.sidebar.error("❌ Lowest grade cannot be higher than highest grade!")
    st.stop()

if current_sem > 8:
    st.sidebar.error("❌ Semester must be between 1-8!")
    st.stop()

# Calculate completed credits
completed_credits = sum(sum(course_structure[sem]) for sem in range(1, current_sem))
current_grade_points = current_cpi * completed_credits

# Run simulation
mean_grade = (lowest_grade + highest_grade) / 2
std_dev = (highest_grade - lowest_grade) / 4

cpi_trajectories = np.zeros((num_simulations, 9))
cpi_trajectories[:, current_sem] = current_cpi

for sim in range(num_simulations):
    total_grade_points = current_grade_points
    total_credits_calc = completed_credits
    
    for sem in range(current_sem, 9):
        semester_credits = course_structure[sem]
        semester_grades = np.random.normal(mean_grade, std_dev, len(semester_credits))
        semester_grades = np.clip(semester_grades, 4, 10)
        
        for grade, credit in zip(semester_grades, semester_credits):
            total_grade_points += grade * credit
            total_credits_calc += credit
        
        final_cpi = total_grade_points / total_credits_calc
        cpi_trajectories[sim, sem] = final_cpi

final_cpis = cpi_trajectories[:, 8]

# Calculate statistics
mean_final_cpi = np.mean(final_cpis)
std_final_cpi = np.std(final_cpis)
median_final_cpi = np.median(final_cpis)
min_final_cpi = np.min(final_cpis)
max_final_cpi = np.max(final_cpis)

ci_95_lower = np.percentile(final_cpis, 2.5)
ci_95_upper = np.percentile(final_cpis, 97.5)

# Display Key Statistics
st.header("📈 Final CPI Statistics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Mean CPI", f"{mean_final_cpi:.4f}")
with col2:
    st.metric("Median CPI", f"{median_final_cpi:.4f}")
with col3:
    st.metric("Std Dev", f"{std_final_cpi:.4f}")
with col4:
    st.metric("Min CPI", f"{min_final_cpi:.4f}")
with col5:
    st.metric("Max CPI", f"{max_final_cpi:.4f}")

# 95% Confidence Interval Box
st.markdown("---")
col_ci1, col_ci2 = st.columns([1, 2])
with col_ci1:
    st.info(f"""
    ### 95% Confidence Interval
    **Lower Bound:** {ci_95_lower:.4f}
    
    **Upper Bound:** {ci_95_upper:.4f}
    
    **Range:** {ci_95_upper - ci_95_lower:.4f}
    """)

with col_ci2:
    st.warning(f"""
    **Interpretation:** There is a 95% probability that your final CPI will fall between **{ci_95_lower:.4f}** and **{ci_95_upper:.4f}**
    
    Current CPI: **{current_cpi:.4f}**
    
    Expected Change: **{mean_final_cpi - current_cpi:+.4f}**
    """)

st.markdown("---")

# Visualizations
st.header("📊 Visualizations")

# Tab 1: CPI Evolution
tab1, tab2, tab3, tab4 = st.tabs(["CPI Evolution", "Final Distribution", "Semester Analysis", "Statistics"])

with tab1:
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot sample simulations
    sample_indices = np.arange(0, num_simulations, max(1, num_simulations // 100))
    for idx in sample_indices:
        ax.plot(range(current_sem, 9), cpi_trajectories[idx, current_sem:9], 
                alpha=0.1, color='blue', linewidth=0.8)
    
    # Mean trajectory
    mean_trajectory = np.mean(cpi_trajectories[:, current_sem:9], axis=0)
    ax.plot(range(current_sem, 9), mean_trajectory, color='red', linewidth=3, 
            label='Mean CPI Trajectory', marker='o', markersize=8)
    
    # 95% CI envelope
    ci_lower_traj = np.array([np.percentile(cpi_trajectories[:, sem], 2.5) for sem in range(current_sem, 9)])
    ci_upper_traj = np.array([np.percentile(cpi_trajectories[:, sem], 97.5) for sem in range(current_sem, 9)])
    ax.fill_between(range(current_sem, 9), ci_lower_traj, ci_upper_traj, 
                    alpha=0.3, color='green', label='95% Confidence Interval')
    
    ax.axhline(current_cpi, color='orange', linestyle='--', linewidth=2, 
               label=f'Current CPI: {current_cpi:.4f}')
    
    ax.set_xlabel('Semester', fontsize=12, fontweight='bold')
    ax.set_ylabel('CPI', fontsize=12, fontweight='bold')
    ax.set_title(f'CPI Evolution Across {num_simulations:,} Simulations', fontsize=13, fontweight='bold')
    ax.set_xticks(range(current_sem, 9))
    ax.legend(loc='best', fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_ylim(min(current_cpi - 1, ci_95_lower - 0.5), max(current_cpi + 1, ci_95_upper + 0.5))
    
    st.pyplot(fig)
    plt.close()

with tab2:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    ax1.hist(final_cpis, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.axvline(mean_final_cpi, color='red', linestyle='--', linewidth=2.5, 
                label=f'Mean: {mean_final_cpi:.4f}')
    ax1.axvline(median_final_cpi, color='green', linestyle='--', linewidth=2.5, 
                label=f'Median: {median_final_cpi:.4f}')
    ax1.axvline(ci_95_lower, color='purple', linestyle=':', linewidth=2, 
                label=f'95% CI')
    ax1.axvline(ci_95_upper, color='purple', linestyle=':', linewidth=2)
    ax1.set_xlabel('Final CPI', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Probability Density', fontsize=11, fontweight='bold')
    ax1.set_title('Distribution of Final CPI', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)
    
    # CDF
    sorted_cpis = np.sort(final_cpis)
    cumulative = np.arange(1, len(sorted_cpis) + 1) / len(sorted_cpis) * 100
    ax2.plot(sorted_cpis, cumulative, linewidth=2.5, color='darkblue')
    ax2.axvline(ci_95_lower, color='purple', linestyle='--', linewidth=2, 
                label=f'2.5th %ile: {ci_95_lower:.4f}')
    ax2.axvline(ci_95_upper, color='purple', linestyle='--', linewidth=2, 
                label=f'97.5th %ile: {ci_95_upper:.4f}')
    ax2.axhline(50, color='green', linestyle=':', alpha=0.5, linewidth=1.5)
    ax2.set_xlabel('Final CPI', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Cumulative Probability (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Cumulative Distribution Function', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)
    
    st.pyplot(fig)
    plt.close()

with tab3:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    box_data = [cpi_trajectories[:, sem] for sem in range(current_sem, 9)]
    bp = ax.boxplot(box_data, labels=[f'Sem {sem}' for sem in range(current_sem, 9)], 
                    patch_artist=True, showmeans=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightcoral')
    
    ax.set_xlabel('Semester', fontsize=12, fontweight='bold')
    ax.set_ylabel('CPI', fontsize=12, fontweight='bold')
    ax.set_title('CPI Distribution by Semester', fontsize=13, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    
    st.pyplot(fig)
    plt.close()

with tab4:
    st.subheader("Semester-by-Semester Breakdown")
    
    semester_data = []
    for sem in range(current_sem, 9):
        cpi_at_sem = cpi_trajectories[:, sem]
        sem_mean = np.mean(cpi_at_sem)
        sem_std = np.std(cpi_at_sem)
        sem_lower = np.percentile(cpi_at_sem, 2.5)
        sem_upper = np.percentile(cpi_at_sem, 97.5)
        
        semester_data.append({
            'Semester': f'Sem {sem}',
            'Mean CPI': f'{sem_mean:.4f}',
            'Std Dev': f'{sem_std:.4f}',
            '95% CI Lower': f'{sem_lower:.4f}',
            '95% CI Upper': f'{sem_upper:.4f}',
            'Total Credits': sum(course_structure[sem]),
            'Avg Grade': f'{mean_grade:.2f}'
        })
    
    df = pd.DataFrame(semester_data)
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Summary Statistics")
    summary_data = {
        'Statistic': ['Mean CPI', 'Median CPI', 'Std Dev', 'Min CPI', 'Max CPI', '95% CI Lower', '95% CI Upper', 'CI Range'],
        'Value': [f'{mean_final_cpi:.4f}', f'{median_final_cpi:.4f}', f'{std_final_cpi:.4f}', 
                  f'{min_final_cpi:.4f}', f'{max_final_cpi:.4f}', f'{ci_95_lower:.4f}', 
                  f'{ci_95_upper:.4f}', f'{ci_95_upper - ci_95_lower:.4f}']
    }
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True)

st.markdown("---")
st.markdown("""
### 📝 About This Simulator
- **Total Course Credits:** {:.0f}
- **Simulations Run:** {:,}
- **Current Completed Credits:** {:.0f}
- **Grade Range:** [{} = {:.1f}, {} = {:.1f}]
- **Expected Average Grade:** {:.2f}
""".format(total_credits, num_simulations, completed_credits, lowest_grade_letter, lowest_grade, highest_grade_letter, highest_grade, mean_grade))

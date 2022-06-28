library(RSQLite)
library(ggplot2)
library(dplyr)
library(tidyr)


# Consume the dataset
con <- dbConnect(SQLite(), "csssa2022.db")
df.sims <- dbReadTable(con, "simulations")
df.summaries <- dbReadTable(con, "summaries")
dbDisconnect(con)

# Setup factors for simulations
df.sims$uuid_exp <- as.factor(df.sims$uuid_exp)
df.sims$ensemble_size <- as.factor(df.sims$ensemble_size)
df.sims$simulation_type <- as.factor(df.sims$simulation_type)
df.sims$interaction_type <- as.factor(df.sims$interaction_type)
df.sims$network_type <- as.factor(df.sims$network_type)

# Remove unneeded columns
df.sims <- df.sims[ , -which(names(df.sims) %in% c("ensemble_size","n","interactants","max_steps"))]

# Remove duplicated
unique_rows <- !duplicated(df.summaries)
df.summaries <- df.summaries[unique_rows,]

# Setup factors for summaries
df.summaries$uuid_exp <- as.factor(df.summaries$uuid_exp)
df.summaries$ensemble_id <- as.factor(df.summaries$ensemble_id)

# Join dataframes per uuid with their features
df_raw <- merge(df.sims, df.summaries, by='uuid_exp')

# Dataset 1: get averages per uuid_exp
df_means <- df_raw %>%
  group_by(simulation_type, interaction_type, network_type, initial_state, step_id) %>%
  summarise_at(c("avg_f"), mean)

df_means <- df_means %>% mutate(mxi = 
                                  case_when(simulation_type == "matrix" & interaction_type == "('dyn',)" ~ "Matrix dyadic",
                                            simulation_type == "abm" & interaction_type == "('dyn',)" ~ "ABM dyadic",
                                            simulation_type == "matrix" & interaction_type == "hord" ~ "Matrix h-order",
                                            simulation_type == "abm" & interaction_type == "hord" ~ "ABM h-order"))

# Dataset 2: get convergence data
df_convergence <- df_raw %>%
  group_by(uuid_exp, simulation_type, interaction_type, network_type, initial_state, ensemble_id) %>%
  summarise_at(c("conv_step"), max)

df_convergence <- df_convergence %>% mutate(mxi = 
                                              case_when(simulation_type == "matrix" & interaction_type == "('dyn',)" ~ "Matrix dyadic",
                                                        simulation_type == "abm" & interaction_type == "('dyn',)" ~ "ABM dyadic",
                                                        simulation_type == "matrix" & interaction_type == "hord" ~ "Matrix h-order",
                                                        simulation_type == "abm" & interaction_type == "hord" ~ "ABM h-order"))

# Dataset 3: yes/no data
df_opinion_convergence <-merge(x = df_convergence, y=df_raw, by=c("uuid_exp", "simulation_type", "interaction_type", "network_type", "initial_state", "ensemble_id"))
df_opinion_convergence <- df_opinion_convergence[df_opinion_convergence$conv_step.x == df_opinion_convergence$step_id,]

df_avg_opinions <- df_opinion_convergence %>%
  group_by(simulation_type, interaction_type, network_type, initial_state) %>%
  summarise_at(c("total_yes", "total_no"), mean)

# Plots

initial_states <- unique(df.sims$initial_state)
network_types <- unique(df.sims$network_type)

# Average magnetization
for (ist in initial_states) {
    df.local <- subset(df_means, initial_state == ist)
    
    ggplot(df.local, aes(x=step_id, color=mxi)) + 
      geom_line(aes(y=2*avg_f - 1)) + 
      facet_grid(vars(network_type)) +
      ggtitle(sprintf("Average magnetization, %.2f", ist)) +
      xlab("Step") +
      ylab(expression(paste("<", M, ">"))) +
      ylim(-1.0, 1.0) +
      theme_classic() + 
      theme(plot.title = element_text(hjust = 0.5))
    ggsave(sprintf("avg_f_%.2f_ist.png", ist))
}

for (nt in network_types) {
  df.local <- subset(df_means, network_type == nt)
  
  ggplot(df.local, aes(x=step_id, color=mxi)) + 
    geom_line(aes(y=2*avg_f - 1)) + 
    facet_grid(vars(initial_state)) +
    ggtitle(sprintf("Average magnetization, %s", nt)) +
    xlab("Step") +
    ylab(expression(paste("<", M, ">"))) +
    ylim(-1.0, 1.0) +
    theme_classic() + 
    theme(plot.title = element_text(hjust = 0.5))
  ggsave(sprintf("avg_f_%s_net.png", nt))
}

# Convergence
for (ist in initial_states) {
  df.local <- subset(df_convergence, initial_state == ist)
  
  ggplot(df.local, aes(x=conv_step, color=mxi, fill=mxi)) + 
    geom_histogram(binwidth=1, alpha=0.35, position="identity") +
    facet_grid(vars(network_type)) +
    ggtitle(sprintf("Convergence time, %.2f", ist)) +
    xlab("Step") +
    ylab("Count") +
    theme_classic() + 
    theme(plot.title = element_text(hjust = 0.5))
  ggsave(sprintf("conv_t_%.2f_ist.png", ist))
}

for (nt in network_types) {
  df.local <- subset(df_convergence, network_type == nt)
  
  ggplot(df.local, aes(x=conv_step, color=mxi, fill=mxi)) + 
    geom_histogram(binwidth=1, alpha=0.35) +
    facet_grid(vars(initial_state)) +
    ggtitle(sprintf("Convergence time, %s", nt)) +
    xlab("Step") +
    ylab("Count") +
    theme_classic() + 
    theme(plot.title = element_text(hjust = 0.5))
  ggsave(sprintf("conv_t_%s_net.png", nt))
}

# Interesting individual ensembles
df_raw_labeled <- df_raw %>% mutate(mxi = 
                                      case_when(simulation_type == "matrix" & interaction_type == "('dyn',)" ~ "Matrix dyadic",
                                                simulation_type == "abm" & interaction_type == "('dyn',)" ~ "ABM dyadic",
                                                simulation_type == "matrix" & interaction_type == "hord" ~ "Matrix h-order",
                                                simulation_type == "abm" & interaction_type == "hord" ~ "ABM h-order"))

# l2dr: 

df.local <- subset(df_raw_labeled, network_type == "l2dr" & initial_state == 0.25)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.25 - l2dr")) +
  xlab("Step") +
  ylab(expression(paste("<", M, ">"))) +
  ylim(-1.0, 1.0) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("l2dr_0.25_net.png")

df.local <- subset(df_raw_labeled, network_type == "l2dr" & initial_state == 0.50)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.5 - l2dr")) +
  xlab("Step") +
  ylab(expression(paste("<", M, ">"))) +
  ylim(-1.0, 1.0) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("l2dr_0.5_net.png")


df.local <- subset(df_raw_labeled, network_type == "l2dr" & initial_state == 0.75)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.75 - l2dr")) +
  xlab("Step") +
  ylab(expression(paste("<", M, ">"))) +
  ylim(-1.0, 1.0) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("l2dr_0.75_net.png")

df.local <- subset(df_raw_labeled, network_type == "l2dr" & initial_state == 0.80)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.80 - l2dr")) +
  xlab("Step") +
  ylab(expression(paste("<", M, ">"))) +
  ylim(-1.0, 1.0) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("l2dr_0.80_net.png")

# 0.5

df.local <- subset(df_raw_labeled, network_type == "hc" & initial_state == 0.50)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.5 - hc")) +
  xlab("Step") +
  ylab("Count") +
  ylab(expression(paste("<", M, ">"))) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("hc_0.5_net.png")


df.local <- subset(df_raw_labeled, network_type == "pl" & initial_state == 0.50)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.5 - pl")) +
  xlab("Step") +
  ylab(expression(paste("<", M, ">"))) +
  ylim(-1.0, 1.0) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("pl_0.5_net.png")

df.local <- subset(df_raw_labeled, network_type == "er" & initial_state == 0.50)

ggplot(df.local, aes(x=step_id, y=2*avg_f-1, color=mxi)) + 
  geom_point(alpha=0.60, size=0.25) +
  ggtitle(sprintf("Average magnetization, 0.5 - er")) +
  xlab("Step") +
  ylab(expression(paste("<", M, ">"))) +
  ylim(-1.0, 1.0) +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5))
ggsave("er_0.5_net.png")

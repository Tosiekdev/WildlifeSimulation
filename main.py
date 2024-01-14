from src.model import SimulationModel


def main():
    model = SimulationModel(
        one_week=100,
        initial_plant=7000,
        initial_hare=14,
        initial_fox=4,
        initial_number_of_hares_habitats=14,
        initial_number_of_foxes_habitats=4,
        food_amount=80,
        food_lifetime=5000, # 5 years
        food_frequency=10,
        fox_mating_season=1000,
        fox_min_mating_range=1,
        fox_max_mating_range=11,
        hare_mating_season=340,
        hare_min_mating_range=3,
        hare_max_mating_range=5,
        hare_lifetime=4000, # 4 years
        hare_consumption=10,
        hare_speed=2,
        hare_trace=2,
        hare_view_range=7,
        hare_view_angle=350,
        hare_hearing_range=10,
        hare_sprint_speed=6,
        hare_sprint_duration=4,
        hare_sprint_cool_down=5,
        hare_sprint_distance=4,
        hare_no_movement_distance=5,
        hare_no_movement_duration=3,
        fox_lifetime=3000, # 3 years
        fox_consumption=4, # 1 hare per week
        fox_speed=2,
        fox_trace=5,
        fox_view_range=20, #10,
        fox_view_angle=135,
        fox_smelling_range=60, #20,
        fox_attack_range=10,
        fox_sprint_speed=5,
        fox_sneak_speed=1,
        pheromone_evaporation_rate=0.1,
        pheromone_diffusion_rate=0.1,
        vaccine_amount=50,
        vaccine_frequency=1000,
        vaccine_effectiveness=1500,
        vaccine_lifetime=50,
        iterations=10_000
    )
    model.run_model()

if __name__ == "__main__":
    main()

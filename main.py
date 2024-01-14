from src.model import SimulationModel


def main():
    model = SimulationModel(
        one_week=500,
        initial_plant=35_000,
        initial_hare=27,
        initial_fox=5,
        initial_number_of_hares_habitats=27,
        initial_number_of_foxes_habitats=5,
        food_amount=25,
        food_lifetime=26_000, # 5 years
        food_frequency=10,
        fox_mating_season=5200,
        fox_min_mating_range=1,
        fox_max_mating_range=11,
        hare_mating_season=1400,
        hare_min_mating_range=3,
        hare_max_mating_range=5,
        hare_lifetime=20_800, # 4 years
        hare_consumption=150,
        hare_speed=2,
        hare_trace=2,
        hare_view_range=20,
        hare_view_angle=350,
        hare_hearing_range=60,
        hare_sprint_speed=4,
        hare_sprint_duration=10,
        hare_sprint_cool_down=10,
        hare_sprint_distance=8,
        hare_no_movement_distance=8,
        hare_no_movement_duration=10,
        fox_lifetime=15_600, # 3 years
        fox_consumption=4, # 1 hare per week
        fox_speed=2,
        fox_trace=10,
        fox_view_range=25,
        fox_view_angle=135,
        fox_smelling_range=60,
        fox_attack_range=10,
        fox_sprint_speed=3,
        fox_sneak_speed=1,
        pheromone_evaporation_rate=0.1,
        pheromone_diffusion_rate=0.1,
        vaccine_amount=1,
        vaccine_frequency=10,
        vaccine_effectiveness=2_600,
        vaccine_lifetime=50,
        iterations=10_000
    )
    model.run_model()

if __name__ == "__main__":
    main()

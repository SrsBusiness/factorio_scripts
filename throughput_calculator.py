#!/usr/bin/env python

from enum import Enum
from collections import Counter

class Producer(Enum):
    ASSEMBLY_MACHINE_3      = 'assembly machine 3', 1.25, 4
    CHEMICAL_PLANT          = 'chemical plant', 1, 3
    ELECTRIC_FURNACE        = 'electric furnace', 2, 2
    # Electric mining drills don't actually have a craft speed, default to 1
    ELECTRIC_MINING_DRILL   = 'electric mining drill', 1, 3
    OFFSHORE_PUMP           = 'offshore pump', 1, 0
    PUMPJACK                = 'pumpjack', 1, 2
    REFINERY                = 'refinery', 1, 3
    ROCKET_SILO             = 'rocket_silo', 1, 4

    def __new__(cls, name, craft_speed, max_prod_slots):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.craft_speed = craft_speed
        obj.max_prod_slots = max_prod_slots
        return obj

class Item(Enum):
    # ENUM_NAME                 = name, producer, recipe, yield_count, craft_time

    # Mined (All intermediate)
    COAL                        = 'coal', Producer.ELECTRIC_MINING_DRILL, {}, 1, 2
    COPPER_ORE                  = 'copper ore', Producer.ELECTRIC_MINING_DRILL, {}, 1, 2
    IRON_ORE                    = 'iron ore', Producer.ELECTRIC_MINING_DRILL, {}, 1, 2
    STONE                       = 'stone', Producer.ELECTRIC_MINING_DRILL, {}, 1, 2

    # Fluid
    CRUDE_OIL                   = 'oil', Producer.PUMPJACK, {}, 0, 0
    WATER                       = 'water', Producer.OFFSHORE_PUMP, {}, 1200, 1
    PETROLEUM_GAS               = 'petroleum gas', Producer.REFINERY, {}, 0, 0
    LIGHT_OIL                   = 'light oil', Producer.REFINERY, {}, 0, 0
    HEAVY_OIL                   = 'heavy oil', Producer.REFINERY, {}, 0, 0

    # Smelted (All intermediate)
    COPPER_PLATE                = 'copper plate', Producer.ELECTRIC_FURNACE, {'COPPER_ORE': 1}, 1, 3.2
    IRON_PLATE                  = 'iron plate', Producer.ELECTRIC_FURNACE, {'IRON_ORE': 1}, 1, 3.2
    STONE_BRICK                 = 'stone brick', Producer.ELECTRIC_FURNACE, {'STONE': 2}, 1, 3.2
    STEEL_PLATE                 = 'steel plate', Producer.ELECTRIC_FURNACE, {'IRON_PLATE': 5}, 1, 16

    # Chemically synthesized
    SULFUR                      = 'sulfur', Producer.CHEMICAL_PLANT, {'WATER': 30, 'PETROLEUM_GAS': 30}, 2, 1
    PLASTIC_BAR                 = 'plastic bar', Producer.CHEMICAL_PLANT, {'COAL': 1, 'PETROLEUM_GAS': 20}, 2, 1
    SULFURIC_ACID               = 'sulfuric acid', Producer.CHEMICAL_PLANT, {'IRON_PLATE': 1, 'SULFUR': 5, 'WATER': 100}, 50, 1
    BATTERY                     = 'battery', Producer.CHEMICAL_PLANT, {'IRON_PLATE': 1, 'COPPER_PLATE': 1, 'SULFURIC_ACID': 20}, 1, 4
    LUBRICANT                   = 'lubricant', Producer.CHEMICAL_PLANT, {'HEAVY_OIL': 10}, 10, 1
    # Solid fuel from light oil is most efficient
    SOLID_FUEL                  = 'solid_fuel', Producer.CHEMICAL_PLANT, {'LIGHT_OIL': 10}, 1, 2

    # Assembled
    IRON_STICK                  = 'iron stick', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 1}, 2, 0.5
    IRON_GEAR_WHEEL             = 'iron gear wheel', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 2}, 1, 0.5
    COPPER_CABLE                = 'copper cable', Producer.ASSEMBLY_MACHINE_3, {'COPPER_PLATE': 1}, 2, 0.5
    ELECTRONIC_CIRCUIT          = 'electronic circuit', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 1, 'COPPER_CABLE': 3}, 1, 0.5
    ADVANCED_CIRCUIT            = 'advanced circuit', Producer.ASSEMBLY_MACHINE_3, {'PLASTIC_BAR': 2, 'COPPER_CABLE': 4, 'ELECTRONIC_CIRCUIT': 2}, 1, 6
    PROCESSING_UNIT             = 'processing unit', Producer.ASSEMBLY_MACHINE_3, {'ELECTRONIC_CIRCUIT': 20, 'ADVANCED_CIRCUIT': 2, 'SULFURIC_ACID': 5}, 1, 10
    TRANSPORT_BELT              = 'transport belt', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 1, 'IRON_GEAR_WHEEL': 1}, 2, 0.5
    PIPE                        = 'pipe', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 1}, 1, 0.5
    ENGINE_UNIT                 = 'engine unit', Producer.ASSEMBLY_MACHINE_3, {'STEEL_PLATE': 1, 'IRON_GEAR_WHEEL': 1, 'PIPE': 2}, 1, 10
    ELECTRIC_ENGINE_UNIT        = 'electric engine unit', Producer.ASSEMBLY_MACHINE_3, {'ELECTRONIC_CIRCUIT': 2, 'ENGINE_UNIT': 1, 'LUBRICANT': 15}, 1, 10
    INSERTER                    = 'inserter', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 1, 'IRON_GEAR_WHEEL': 1, 'ELECTRONIC_CIRCUIT': 1}, 1, 0.5
    WALL                        = 'wall', Producer.ASSEMBLY_MACHINE_3, {'STONE_BRICK': 5}, 1, 0.5
    GRENADE                     = 'grenade', Producer.ASSEMBLY_MACHINE_3, {'COAL': 10, 'IRON_PLATE': 5}, 1, 8
    FIREARM_MAGAZINE            = 'firearm magazine', Producer.ASSEMBLY_MACHINE_3, {'IRON_PLATE': 4}, 1, 1
    PIERCING_ROUNDS_MAGAZINE    = 'piercing rounds magazine', Producer.ASSEMBLY_MACHINE_3, {'COPPER_PLATE': 5, 'STEEL_PLATE': 1, 'FIREARM_MAGAZINE': 1}, 1, 3
    RAIL                        = 'rail', Producer.ASSEMBLY_MACHINE_3, {'STONE': 1, 'STEEL_PLATE': 1, 'IRON_STICK': 1}, 2, 0.5
    ELECTRIC_FURNACE            = 'electric furnace', Producer.ASSEMBLY_MACHINE_3, {'STEEL_PLATE': 10, 'ADVANCED_CIRCUIT': 5, 'STONE_BRICK': 10}, 1, 5
    PRODUCTIVITY_MODULE         = 'productivity module', Producer.ASSEMBLY_MACHINE_3, {'ELECTRONIC_CIRCUIT': 5, 'ADVANCED_CIRCUIT': 5}, 1, 15
    FLYING_ROBOT_FRAME          = 'flying robot frame', Producer.ASSEMBLY_MACHINE_3, {'STEEL_PLATE': 1, 'BATTERY': 2, 'ELECTRONIC_CIRCUIT': 3, 'ELECTRIC_ENGINE_UNIT': 1}, 1, 20
    LOW_DENSITY_STRUCTURE       = 'low density structure', Producer.ASSEMBLY_MACHINE_3, {'COPPER_PLATE': 20, 'STEEL_PLATE': 2, 'PLASTIC_BAR': 5}, 1, 20
    SPEED_MODULE                = 'speed module', Producer.ASSEMBLY_MACHINE_3, {'ELECTRONIC_CIRCUIT': 5, 'ADVANCED_CIRCUIT': 5}, 1, 15
    ROCKET_CONTROL_UNIT         = 'rocket control unit', Producer.ASSEMBLY_MACHINE_3, {'PROCESSING_UNIT': 1, 'SPEED_MODULE': 1}, 1, 30
    ROCKET_FUEL                 = 'rocket fuel', Producer.ASSEMBLY_MACHINE_3, {'SOLID_FUEL': 10, 'LIGHT_OIL': 10}, 1, 30
    ROCKET_PART                 = 'rocket part', Producer.ROCKET_SILO, {'LOW_DENSITY_STRUCTURE': 10, 'ROCKET_CONTROL_UNIT': 10, 'ROCKET_FUEL': 10}, 1, 3

    #Science Packs
    AUTOMATION_SCIENCE_PACK     = 'automation science pack', Producer.ASSEMBLY_MACHINE_3, {'COPPER_PLATE': 1, 'IRON_GEAR_WHEEL': 1}, 1, 5
    LOGISTIC_SCIENCE_PACK       = 'logistic science pack', Producer.ASSEMBLY_MACHINE_3, {'TRANSPORT_BELT': 1, 'INSERTER': 1}, 1, 6
    MILITARY_SCIENCE_PACK       = 'military science pack', Producer.ASSEMBLY_MACHINE_3, {'PIERCING_ROUNDS_MAGAZINE': 1, 'GRENADE': 1, 'WALL': 2}, 2, 10
    CHEMICAL_SCIENCE_PACK       = 'chemical science pack', Producer.ASSEMBLY_MACHINE_3, {'SULFUR': 1, 'ADVANCED_CIRCUIT': 3, 'ENGINE_UNIT': 2}, 2, 24
    PRODUCTION_SCIENCE_PACK     = 'production science pack', Producer.ASSEMBLY_MACHINE_3, {'RAIL': 30, 'ELECTRIC_FURNACE': 1, 'PRODUCTIVITY_MODULE': 1}, 3, 21
    UTILITY_SCIENCE_PACK        = 'utility science pack', Producer.ASSEMBLY_MACHINE_3, {'PROCESSING_UNIT': 2, 'FLYING_ROBOT_FRAME': 1, 'LOW_DENSITY_STRUCTURE': 3}, 3, 21
    SPACE_SCIENCE_PACK          = 'space science pack', Producer.ROCKET_SILO, {'ROCKET_PART': 100}, 1000, 40.33

    def __new__(cls, name, producer, recipe, yield_count, craft_time):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.producer = producer
        obj.recipe = Counter({
            cls.__members__[item]: count for item, count in recipe.items()
        })
        # yield count is the number of this item its recipe yields
        # E.g. transport belts have yield_count=2 because its recipe
        # (1 iron plate + 1 iron gear wheel) yields 2 transport belts
        obj.yield_count = yield_count
        obj.craft_time = craft_time
        return obj

    @classmethod
    def science_packs(cls):
        return (
            item for item in [
                Item.AUTOMATION_SCIENCE_PACK,
                Item.LOGISTIC_SCIENCE_PACK,
                Item.MILITARY_SCIENCE_PACK,
                Item.CHEMICAL_SCIENCE_PACK,
                Item.PRODUCTION_SCIENCE_PACK,
                Item.UTILITY_SCIENCE_PACK,
                Item.SPACE_SCIENCE_PACK,
            ]
        )

    @property
    def is_not_intermediate(self):
        # Set of Items which whose recipe cannot be boosted by productivity
        # modules
        return self in {
            Item.TRANSPORT_BELT,
            Item.PIPE,
            Item.INSERTER,
            Item.WALL,
            Item.GRENADE,
            Item.FIREARM_MAGAZINE,
            Item.PIERCING_ROUNDS_MAGAZINE,
            Item.RAIL,
            Item.ELECTRIC_FURNACE,
            Item.PRODUCTIVITY_MODULE,
            # Productivity modules in the silo only work on the individual rocket parts
            # The launch itself always requires 100 parts
            Item.SPACE_SCIENCE_PACK
        }

    def __print_recipe_indent(self, count, indent=0):
        ingredients_total = Counter({self: count})
        print(f'{"    " * indent}{self.value}: {count}')
        for i, count_i in self.recipe.items():
            ingredients_total += i.__print_recipe_indent(count * count_i / self.yield_count,  indent + 1)
        return ingredients_total

    def print_recipe(self, count=1):
        for item, count in self.__print_recipe_indent(count).items():
            print(f'{item.value}: {count}')

    # throughput is in units of Hz i.e. items/second
    def __print_throughput_indent(self, throughput, indent=0):
        ingredient_throughputs_total = Counter({self: throughput})
        if self.producer and self.recipe:
            if self.is_not_intermediate:
                productivity = 1
                craft_speed_penalty = 1
            else:
                productivity = 1 + .1 * self.producer.max_prod_slots
                craft_speed_penalty = 1 - .15 * self.producer.max_prod_slots
            craft_speed_adjusted = self.producer.craft_speed * craft_speed_penalty
            producers_required = throughput / (productivity * craft_speed_adjusted * self.yield_count / self.craft_time)
            print(f'{"    " * indent}{self.value}: {throughput}/s, {producers_required} '
                  f'{self.producer.value} with {0 if self.is_not_intermediate else self.producer.max_prod_slots} '
                  f'productivity modules required')
            for i, count_i in self.recipe.items():
                # calculate the throughput for each ingredient and recurse
                throughput_i = throughput / productivity * (count_i / self.yield_count)
                ingredient_throughputs_total += i.__print_throughput_indent(throughput_i, indent + 1)
        else:
            print(f'{"    " * indent}{self.value}: {throughput}/s')
        return ingredient_throughputs_total

    def print_throughput(self, throughput):
        for item, total_throughput in self.__print_throughput_indent(throughput).items():
            print(f'{item.value}: {total_throughput}/s')

if __name__ == '__main__':
    for science in Item.science_packs():
        science.print_throughput(45)
        print()

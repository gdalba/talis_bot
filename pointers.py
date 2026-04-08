import math
import re
import pymem


class Pointers:
    def __init__(self, pid):
        self.pm = pymem.Pymem()
        self.pm.open_process_from_id(pid)
        self.CLIENT = 0x00400000
        
        # ==================== LEGACY POINTERS (Original Game Version) ====================
        #self.DC_POINTER = 0x012CE35C
        self.CHAR_NAME_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x384])
        self.LEVEL_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x32C])
        self.HP_POINTER = self.get_pointer(self.CLIENT +0x00DEAAA0, offsets=[0x320])
        self.HP_PLUS_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x3AC])
        self.HP_BUFF_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x3A8])
        #self.GOLD_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x410])

        #self.MANA_BUFF_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x6F0])

        self.X_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x6F8])
        self.Y_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x6FC])

        self.BATTLE_STATUS_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x73C])
        #self.SIT_POINTER = self.get_pointer(self.CLIENT + 0x00DEAAA0, offsets=[0x290])

        #self.TARGET_SELECT = self.get_pointer(self.CLIENT + 0x0102EA20, offsets=[0x50, 0x0, 0xDC, 0x24, 0x3BC, 0xD0])
        #self.TARGET_HP_POINTER = self.get_pointer(0x0103B508, offsets=[0x5900, 0x4A4, 0xA34, 0xC, 0x4, 0x1274, 0x18])        
        #self.TARGET_SELECT = self.resolve_pointer_chain_vc(0x0102EA20, offsets=[0x50, 0x0, 0xDC, 0x24, 0x3BC, 0xD0])

        self.TARGET_NAME_POINTER = self.get_pointer(0x0103B508, offsets=[0x23AC, 0xA30, 0x630, 0xC, 0x0, 0x314, 0x18])

        self.TEAM_SIZE_POINTER = self.get_pointer(0x0106D328, offsets=[0x3D8])
        self.TEAM_NAME_1 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x77C, 0x0, 0xC, 0x678, 0x8B4])
        self.TEAM_NAME_2 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x34C, 0x0, 0xC, 0x678, 0x8B4])
        self.TEAM_NAME_3 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x3F4, 0x0, 0xC, 0x1F4, 0x15C])
        self.TEAM_NAME_4 = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xA1C, 0x0, 0xC, 0x1F4, 0x54])

        self.BAG_OPEN_POINTER = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x5C4, 0x0, 0xC, 0x1F8, 0x42C, 0xBA0])
        self.BAG_1 = self.get_pointer(0x011450EC, offsets=[0x838, 0xC4, 0x0, 0x8, 0x10])
        self.BAG_2 = self.get_pointer(0x011450EC, offsets=[0x838, 0xC4, 0x4, 0x8, 0x10])
        self.MOUNT_STATUS_POINTER = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0x8B0])
        #self.BUFFS_QUANTITY_POINTER = self.get_pointer(self.CLIENT + 0x00C20980, offsets=[0xCBC])

        # self.LOOT_POINTER = self.get_pointer(0x012C05C8, offsets=[0xD0, 0x7F4, 0x0, 0x24, 0x40])
        #self.LOOT_POINTER = self.get_pointer(self.CLIENT + 0x00EC05C8, offsets=[0xD0, 0x7F4, 0x0, 0x24, 0x40])
        #self.LOOT_WINDOW = 0x0105B958

        #self.FIRST_LINK_SUR = self.get_pointer(0x012CE2DC, offsets=[0x18, 0x8C, 0x3C])

        self.TARGET_ID = 0x115CB20
        self.base = 0x0107C6B0
        self.basei = 0x0

        # Limites para busca bidirecional
        self.BASE_MIN = 0x0000CE00  # Limite inferior para busca
        self.BASE_MAX = 0x0EFFFFFF  # Limite superior para busca
    def get_pointer(self, base_address, offsets):
        """
        Calcula o ponteiro final seguindo uma cadeia de offsets.
        """
        try:
            address = base_address
            for offset in offsets:  # Navega pelos offsets até o endereço final
                address = self.pm.read_int(address) + offset
            return address
        except Exception as e:
            print(f"Erro ao calcular o ponteiro {base_address} / {offsets}: {e}")
            return None

    def resolve_pointer_chain_vc(self, base_address, offsets):
        """
        Resolve chain using the same style as scanner vc:
        addr = read_int(base)
        for each offset except last: addr = read_int(addr + offset)
        final = addr + last_offset
        """
        try:
            if not offsets:
                return base_address

            addr = self.pm.read_int(base_address)
            for offset in offsets[:-1]:
                addr = self.pm.read_int(addr + offset)

            return addr + offsets[-1]
        except Exception:
            return None
    def read_value(self, address, data_type="byte"):
        try:
            if data_type == "byte":
                return self.pm.read_bytes(address, 1)[0]  # Lê 1 byte
            elif data_type == "int":
                return self.pm.read_int(address)  # Lê 4 bytes como inteiro
            elif data_type == "float":
                return self.pm.read_float(address)  # Lê 4 bytes como float
            else:
                print(f"Tipo de dado desconhecido: {data_type}")
                return None
        except Exception as e:
            #print(f"Erro ao ler valor ({data_type}): {e}")
            return None

    def read_string_from_pointer(self, base_pointer, offset=0, max_length=50):
        try:
            pointer_address = self.pm.read_int(base_pointer)
            final_address = pointer_address + offset
            byte_data = self.pm.read_bytes(final_address, max_length)
            string_data = byte_data.split(b'\x00', 1)[0].decode('utf-8', errors='ignore')
            return string_data
        except Exception as e:
            print(f"String Error: {e}")
            return "Offline Account"

    def read_string_direct(self, address, max_length=50):
        """
        Lê uma string diretamente de um endereço (sem seguir ponteiro)
        """
        try:
            byte_data = self.pm.read_bytes(address, max_length)
            string_data = byte_data.split(b'\x00', 1)[0].decode('utf-8', errors='ignore')
            return string_data
        except Exception as e:
            # print(f"String Error: {e}")
            return "Offline Account"

    def get_char_name(self):        
        if self.CHAR_NAME_POINTER:
            try:
                name = self.read_string_direct(self.CHAR_NAME_POINTER, max_length=50)
                if name and re.match(r"^[\w]+$", name):
                    return name
            except:
                pass
        
        # Fallback to legacy pointer
        name = self.read_string_from_pointer(self.CHAR_NAME_POINTER, offset=0xBC, max_length=50)

        if re.match(r"^[\w]+$", name):  # Alfanumérico
            return name

        # Segunda tentativa
        pointer = self.get_pointer(self.CLIENT + 0x00D450EC, offsets=[0xBC])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def get_target_name(self):  # modificado, invertido ordem
        # Primeira tentativa: ler ponteiro com offset 0
        pointer_address = self.pm.read_int(self.TARGET_NAME_POINTER)        
        pointer_address = pointer_address + 0x9AC
        name = self.read_string_from_pointer(pointer_address, offset=0x0, max_length=100)
        # print(f"name 1 com offset 0 = {name}")

        # se der erro, ler normal
        if name == "Offline Account":
            # Segunda tentativa: ler diretamente do ponteiro + 0x9AC
            pointer_address = self.pm.read_int(self.TARGET_NAME_POINTER)
            name = self.read_string_from_pointer(pointer_address, offset=0x9AC, max_length=100)
            # print(f"name original try 2= {name}")

        # Verifica se o nome é alfanumérico (como no Lua)
        if re.match(r"^[\w ']+$", name):
            return name
        else:
            # terceira tentativa: ler diretamente do ponteiro + 0x9AC
            second_name = self.read_string_from_pointer(self.TARGET_NAME_POINTER, offset=0x9AC, max_length=100)
            # print(f"name original try 3= {second_name}")
            if second_name:
                return second_name

    def team_name_1(self):
        name = self.read_string_from_pointer(self.TEAM_NAME_1, offset=0x4F4, max_length=50)

        if re.match(r"^[\w]+$", name):  # Alfanumérico
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x77C, 0x0, 0xC, 0x678, 0x8B4, 0x4F4])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def team_name_2(self):
        name = self.read_string_from_pointer(self.TEAM_NAME_2, offset=0x4F4, max_length=50)
        if re.match(r"^[\w]+$", name):
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x34C, 0x0, 0xC, 0x678, 0x8B4, 0x4F4])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def team_name_3(self):
        name = self.read_string_from_pointer(self.TEAM_NAME_3, offset=0x54, max_length=50)
        if re.match(r"^[\w]+$", name):
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0x3F4, 0x0, 0xC, 0x1F4, 0x15C, 0x54])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def team_name_4(self):
        name = self.read_string_from_pointer(self.TEAM_NAME_4, offset=0x54, max_length=50)
        if re.match(r"^[\w]+$", name):
            return name
        pointer = self.get_pointer(0x012CE2E0, offsets=[0x18, 0xA1C, 0x0, 0xC, 0x1F4, 0x54, 0x54])
        if pointer:
            name = self.read_string_from_pointer(pointer, offset=0x0, max_length=50)
        return name

    def get_level(self):
        return self.read_value(self.LEVEL_POINTER, data_type="byte")

    def is_target_selected(self):
        print(self.TARGET_SELECT)
        if self.TARGET_SELECT is None:
            print("Erro: Ponteiro TARGET_SELECT não calculado.")
            return False

        target = self.read_value(self.TARGET_SELECT, data_type="byte")  # Lê 1 byte
        if target == 1:
            #print("Target selected")
            return True
        return False

    def target_hp(self):
        hp = self.read_value(self.TARGET_HP_POINTER, data_type="int")
        return hp

    def target_hp_full(self):
        return self.read_value(self.TARGET_HP_POINTER, data_type="int") == 597

    def is_target_dead(self):
        dead = self.read_value(self.TARGET_HP_POINTER, data_type="int")
        if dead == 0:
            return True

    def get_hp(self):
        # New pointer returns current HP directly
        return self.read_value(self.HP_POINTER, data_type="int")

    def get_hp_plus(self):
        plus = self.read_value(self.HP_PLUS_POINTER, data_type="byte")
        if plus is None:
            return None
        if plus >= 100:
            return plus - 100
        else:
            return plus

    def get_hp_buff(self):
        return self.read_value(self.HP_BUFF_POINTER, data_type="int")

    def get_mana(self):
        # New pointer returns current mana directly
        return self.read_value(self.MANA_POINTER, data_type="int")

    def get_mana_buff(self):
        return self.read_value(self.MANA_BUFF_POINTER, data_type="int")

    def get_max_mana(self):
        """
        Returns the maximum Mana. Since Max Mana isn't stored directly in this game version,
        we use a caching approach: track the highest Mana value seen.
        When character has full mana, current mana = max mana.
        """
        current_mana = self.get_mana()
        if current_mana is not None and current_mana > self._cached_max_mana:
            self._cached_max_mana = current_mana
        
        # Return cached max if we have it, otherwise return current
        return self._cached_max_mana if self._cached_max_mana > 0 else current_mana

    def set_max_hp(self, value):
        """Manually set the max HP cache (useful for initialization)"""
        self._cached_max_hp = value
    
    def set_max_mana(self, value):
        """Manually set the max mana cache (useful for initialization)"""
        self._cached_max_mana = value

    def is_in_battle(self):
        battle = self.read_value(self.BATTLE_STATUS_POINTER, data_type="byte")
        if battle == 1:
            #print("Battle Status")
            return True

    def is_sitting(self):
        sitting = self.read_value(self.SIT_POINTER, data_type="byte")
        if sitting == 200:
            return True
        else:
            return False

    def get_x(self):
        x = self.read_value(self.X_POINTER, data_type="float") / 20
        return x > 0 and math.floor(x) or math.ceil(x)

    def get_y(self):
        y = self.read_value(self.Y_POINTER, data_type="float") / 20
        return y > 0 and math.floor(y) or math.ceil(y)

    def char_x(self):
        x = self.read_value(self.X_POINTER, data_type="float")
        return x > 0 and math.floor(x) or math.ceil(x)

    def char_y(self):
        y = self.read_value(self.Y_POINTER, data_type="float")
        return y > 0 and math.floor(y) or math.ceil(y)

    def is_bag_open(self):
        bag = self.read_value(self.BAG_OPEN_POINTER, data_type="int")
        if bag == 903:
            return True

    def get_gold(self):
        return self.read_value(self.GOLD_POINTER, data_type="int")

    def bag_1_quantity(self):
        return self.read_value(self.BAG_1, data_type="int")

    def bag_2_quantity(self):
        return self.read_value(self.BAG_2, data_type="int")

    def get_team_size(self):
        team = self.read_value(self.TEAM_SIZE_POINTER, data_type="int")
        if team is None:
            return 0
        else:
            return team

    def get_dc(self):
        dc = self.read_value(self.DC_POINTER, data_type="int")
        return dc

    def mount(self):
        mount = self.read_value(self.MOUNT_STATUS_POINTER, data_type="int")
        # print(f"Mount: {mount}")
        return mount

    def get_target_id(self):
        id = self.read_value(self.TARGET_ID, data_type="int")
        # print(f"Target ID: {id}")
        if id is None:
            print("Erro ao ler ID")
            return None  # Retorna None de forma explícita para evitar erros

        try:
            return hex(id)[2:].upper()
        except Exception as e:
            print(f"Erro ao converter ID para hexadecimal: {e}")
            return None  # Retorna None se houver qualquer erro na conversão

    def get_id(self):
        id = self.read_value(self.TARGET_ID, data_type="int")
        # print(f"ID: {id}")
        return id


    def search_id(self):
        final_pointer = 0
        max_attempts = 3  # Número máximo de tentativas completas
        erro_count = 0  # Contador para limitar mensagens de erro

        for attempt in range(max_attempts):
            try:
                # Obtém o ID do alvo
                targetid = self.get_target_id()
                if targetid is None:
                    print("Reiniciando busca: ID do alvo não encontrado")
                    continue  # Passa para a próxima tentativa

                found = False
                erro_count = 0  # Reinicia contador de erros para cada nova tentativa

                # Busca crescente (do base atual até BASE_MAX)
                current_base = self.base
                while current_base <= self.BASE_MAX:
                    # Lê o valor no endereço base atual
                    a = self.read_value(current_base + self.basei, "int")
                    if a is None:
                        # Limita mensagens de erro
                        erro_count += 1
                        if erro_count <= 1:
                            print("Erro de leitura na busca crescente, pulando para próxima tentativa...")
                        # Reinicia a busca completamente em vez de continuar com erros
                        break

                    b = a + 0x8

                    # Lê o valor no endereço calculado
                    c_value = self.read_value(b, "int")
                    if c_value is None:
                        # Avança para o próximo endereço sem mostrar erro
                        current_base += 0x4
                        continue

                    c = hex(c_value)[2:].upper()

                    if c == targetid:
                        final_pointer = current_base
                        found = True
                        break
                    else:
                        current_base += 0x4

                # Se houve erro na busca crescente, reinicia a tentativa
                if erro_count > 0:
                    continue

                # Se não encontrou na busca crescente, tenta busca decrescente
                if not found:
                    print("Iniciando busca decrescente...")
                    current_base = self.base - 0x4
                    erro_count = 0  # Reinicia contador para a busca decrescente

                    while current_base >= self.BASE_MIN:
                        # Lê o valor no endereço base atual
                        a = self.read_value(current_base + self.basei, "int")
                        if a is None:
                            # Limita mensagens de erro
                            erro_count += 1
                            if erro_count <= 1:
                                print("Erro de leitura na busca decrescente, pulando para próxima tentativa...")
                            # Reinicia a busca completamente em vez de continuar com erros
                            break

                        b = a + 0x8

                        # Lê o valor no endereço calculado
                        c_value = self.read_value(b, "int")
                        if c_value is None:
                            # Avança para o próximo endereço sem mostrar erro
                            current_base -= 0x4
                            continue

                        c = hex(c_value)[2:].upper()

                        if c == targetid:
                            final_pointer = current_base
                            found = True
                            break
                        else:
                            current_base -= 0x4

                # Se houve erro na busca decrescente, reinicia a tentativa
                if erro_count > 0:
                    continue

                # Se encontrou o alvo em qualquer uma das buscas
                if found:
                    # Lê o ponteiro final e as coordenadas em uma única verificação
                    pointer = self.read_value(final_pointer + self.basei, "int")
                    if pointer is None:
                        print("Reiniciando: falha ao ler ponteiro final")
                        continue

                    # Lê as coordenadas X e Y
                    x_value = self.read_value(pointer + 0x810, "float")
                    y_value = self.read_value(pointer + 0x814, "float")

                    # Verifica se ambas as coordenadas foram lidas com sucesso
                    if x_value is None or y_value is None:
                        print("Reiniciando: falha ao ler coordenadas")
                        continue

                    # Calcula as coordenadas finais
                    target_x = int(x_value / 20)
                    target_y = int(y_value / 20)

                    # Atualiza o ponteiro base para a próxima busca
                    self.base = final_pointer

                    # Retorna os valores encontrados
                    return target_x, target_y, pointer
                else:
                    print("Alvo não encontrado, reiniciando busca...")

            except Exception as e:
                print(f"Erro durante a busca: {e}. Reiniciando...")

        # Se chegou aqui, todas as tentativas falharam
        print("Falha em todas as tentativas de busca. Reiniciando o processo...")
        return None, None, None  # Retorna None para indicar falha

    def is_loot(self):
        loot = self.read_value(self.LOOT_POINTER, data_type="int")
        return loot

    def write_position(self, pointer, x, y):
        try:
            basex = pointer + 0x810
            basey = pointer + 0x814

            # print(f"Escrevendo posição - X: {x} em {hex(basex)}, Y: {y} em {hex(basey)}")

            self.pm.write_float(basex, float(x))
            self.pm.write_float(basey, float(y))
            return True

        except Exception as e:
            print(f"Erro ao definir posição: {e}")
            return False

    def write_camera(self, z, r, a):
        zoom = self.ZOOM_POINTER
        rotation = self.ROTATION_POINTER
        angle = self.ANGLE_POINTER
        self.pm.write_float(zoom, float(z))
        self.pm.write_float(rotation, float(r))
        self.pm.write_float(angle, float(a))

    def loot_window(self):
        l = self.read_value(self.LOOT_WINDOW, data_type="int")

        if l is None:
            return 0

        if l == 1:
            return True
        else:
            return False

    def get_sur_info(self):
        info = self.read_string_from_pointer(self.FIRST_LINK_SUR, offset=0x64, max_length=100)
        print(info)

        # Extrai o nome e as coordenadas usando expressões regulares
        name_match = re.search(r'text="([^"]+)\s*\[(-?\d+),(-?\d+)\]"', info)

        if name_match:
            name = name_match.group(1).strip()
            x_coord = name_match.group(2)
            y_coord = name_match.group(3)

            # Retorna um dicionário com as informações formatadas
            return {
                'name': name,
                'coords': f'{x_coord},{y_coord}'
            }

    def confirm_box(self):
        confirm = self.read_value(self.CONFIRM_BOX_POINTER, data_type="int")
        if confirm == 1:
            return True
        else:
            return False

    def get_location(self):

        location = self.read_string_from_pointer(self.LOCATION_POINTER, offset=0x44C, max_length=100)
        if re.match(r"^[\w ']+$", location):
            #print(f"Char location: {location}")
            return location
        else:
            pointer_address = self.pm.read_int(self.LOCATION_POINTER)
            pointer_address = pointer_address + 0x44C
            second_pointer = self.read_string_from_pointer(pointer_address, offset=0x0, max_length=100)
            if second_pointer:
                #print(f"Char location (2): {second_pointer}")
                return second_pointer

    def get_location_2(self):

        location_2 = self.read_string_from_pointer(self.LOCATION_POINTER_2, offset=0x0, max_length=100)

        return location_2


    def get_notification(self):
        pointer = self.read_value(self.NOTIFICATION_POINTER, data_type="int")
        if pointer >= 1:
            print(f"Notification: {pointer}")
            return True
        else:
            return False

    def get_dialog(self):
        dialog = self.read_value(self.DIALOG_POINTER, data_type="int")
        if dialog == 16775:
            return True
        else:
            return False

    def get_sin_combo(self):
        passive = self.read_value(self.SIN_PASSIVE, data_type="int")
        return passive

    def get_monk_combo(self):
        passive = self.read_value(self.MONK_PASSIVE, data_type="int")
        return passive

    def get_system_menu(self):
        system = self.read_value(self.SYSTEM_MENU_POINTER, data_type="int")
        if system == 1610612736:
            return True
        else:
            return False


if __name__ == "__main__":
    import sys
    import argparse
    import time
    import struct

    parser = argparse.ArgumentParser(description="Test memory pointers for a game process")
    parser.add_argument("pid", type=int, help="Process ID (PID) of the game")
    parser.add_argument("--loop", "-l", action="store_true", help="Continuously monitor values")
    parser.add_argument("--interval", "-i", type=float, default=1.0, help="Update interval in seconds (default: 1.0)")
    
    # Scanner modes
    parser.add_argument("--scan", "-s", action="store_true", help="Enter interactive scanner mode")
    parser.add_argument("--search-int", type=int, metavar="VALUE", help="Search for an integer value in memory")
    parser.add_argument("--search-float", type=float, metavar="VALUE", help="Search for a float value in memory")
    parser.add_argument("--search-string", type=str, metavar="TEXT", help="Search for a string in memory")
    parser.add_argument("--dump", type=str, metavar="ADDRESS", help="Dump memory around an address (hex, e.g., 0x12CE35C)")
    parser.add_argument("--dump-size", type=int, default=256, help="Size of memory dump in bytes (default: 256)")
    parser.add_argument("--probe", action="store_true", help="Probe around known pointers for valid data")
    parser.add_argument("--probe-range", type=int, default=0x1000, help="Range to probe around pointers (default: 0x1000)")
    
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Pointers Test - PID: {args.pid}")
    print(f"{'='*60}\n")

    try:
        pm = pymem.Pymem()
        pm.open_process_from_id(args.pid)
        print("[+] Successfully attached to process!\n")
    except Exception as e:
        print(f"[-] Failed to attach to process: {e}")
        sys.exit(1)

    # ==================== SCANNER FUNCTIONS ====================
    
    def get_memory_regions():
        """Get readable memory regions of the process"""
        import ctypes
        from ctypes import wintypes
        
        MEM_COMMIT = 0x1000
        PAGE_READABLE = (0x02 | 0x04 | 0x20 | 0x40 | 0x80)  # Various readable page protections
        
        class MEMORY_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BaseAddress", ctypes.c_size_t),
                ("AllocationBase", ctypes.c_size_t),
                ("AllocationProtect", wintypes.DWORD),
                ("RegionSize", ctypes.c_size_t),
                ("State", wintypes.DWORD),
                ("Protect", wintypes.DWORD),
                ("Type", wintypes.DWORD),
            ]
        
        regions = []
        address = 0x10000  # Start after null page
        max_address = 0x7FFFFFFF  # 32-bit process max
        
        kernel32 = ctypes.windll.kernel32
        handle = pm.process_handle
        
        mbi = MEMORY_BASIC_INFORMATION()
        mbi_size = ctypes.sizeof(mbi)
        
        while address < max_address:
            result = kernel32.VirtualQueryEx(handle, ctypes.c_size_t(address), ctypes.byref(mbi), mbi_size)
            if result == 0:
                break
            
            base_addr = mbi.BaseAddress if mbi.BaseAddress else 0
            region_size = mbi.RegionSize if mbi.RegionSize else 0
            
            if region_size == 0:
                break
            
            if mbi.State == MEM_COMMIT and (mbi.Protect & PAGE_READABLE):
                regions.append((base_addr, region_size))
            
            address = base_addr + region_size
            if address <= base_addr:
                break
        
        return regions
    
    def search_int_value(value, regions=None):
        """Search for a 4-byte integer value in memory"""
        print(f"[*] Searching for integer: {value} (0x{value:X})")
        results = []
        
        if regions is None:
            regions = get_memory_regions()
        
        print(f"[*] Scanning {len(regions)} memory regions...")
        
        value_bytes = struct.pack('<i', value)
        
        for base, size in regions:
            try:
                data = pm.read_bytes(base, size)
                offset = 0
                while True:
                    idx = data.find(value_bytes, offset)
                    if idx == -1:
                        break
                    results.append(base + idx)
                    offset = idx + 1
            except:
                pass
        
        print(f"[+] Found {len(results)} matches")
        return results
    
    def search_float_value(value, tolerance=0.01, regions=None):
        """Search for a float value in memory with tolerance"""
        print(f"[*] Searching for float: {value} (±{tolerance})")
        results = []
        
        if regions is None:
            regions = get_memory_regions()
        
        print(f"[*] Scanning {len(regions)} memory regions...")
        
        for base, size in regions:
            try:
                data = pm.read_bytes(base, size)
                for i in range(0, len(data) - 3, 4):
                    try:
                        f = struct.unpack('<f', data[i:i+4])[0]
                        if abs(f - value) <= tolerance:
                            results.append(base + i)
                    except:
                        pass
            except:
                pass
        
        print(f"[+] Found {len(results)} matches")
        return results
    
    def search_string_value(text, regions=None):
        """Search for a string in memory"""
        print(f"[*] Searching for string: '{text}'")
        results = []
        
        if regions is None:
            regions = get_memory_regions()
        
        print(f"[*] Scanning {len(regions)} memory regions...")
        
        # Search for both ASCII and UTF-8
        text_bytes = text.encode('utf-8')
        
        for base, size in regions:
            try:
                data = pm.read_bytes(base, size)
                offset = 0
                while True:
                    idx = data.find(text_bytes, offset)
                    if idx == -1:
                        break
                    results.append(base + idx)
                    offset = idx + 1
            except:
                pass
        
        print(f"[+] Found {len(results)} matches")
        return results
    
    def dump_memory(address, size=256):
        """Dump memory at an address in hex + ASCII format"""
        print(f"\n[*] Memory dump at 0x{address:08X} ({size} bytes):\n")
        
        try:
            data = pm.read_bytes(address, size)
        except Exception as e:
            print(f"[-] Failed to read memory: {e}")
            return
        
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hex_str = ' '.join(f'{b:02X}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f"  {address + i:08X}  {hex_str:<48}  {ascii_str}")
    
    def probe_around_pointer(name, base_address, probe_range, data_type="int"):
        """Probe around a pointer for valid-looking data"""
        print(f"\n[*] Probing around {name} (0x{base_address:08X}) ±0x{probe_range:X}")
        
        results = []
        start = max(0, base_address - probe_range)
        end = base_address + probe_range
        
        for addr in range(start, end, 4):
            try:
                if data_type == "int":
                    value = pm.read_int(addr)
                    # Look for reasonable integer values (1-999999)
                    if value is not None and 1 <= value <= 999999:
                        results.append((addr, value))
                elif data_type == "float":
                    value = pm.read_float(addr)
                    if value is not None and 0.1 <= abs(value) <= 100000:
                        results.append((addr, value))
                elif data_type == "string":
                    try:
                        data = pm.read_bytes(addr, 20)
                        text = data.split(b'\x00')[0].decode('utf-8', errors='ignore')
                        if len(text) >= 3 and text.isalnum():
                            results.append((addr, text))
                    except:
                        pass
            except:
                pass
        
        return results
    
    def scan_pointer_chain(target_address, max_depth=4, max_offset=0x1000):
        """
        Scan for pointer chains leading to a target address.
        Searches for pointers that point to (target - offset) for various offsets.
        """
        print(f"\n{'='*60}")
        print(f"  Pointer Chain Scanner")
        print(f"{'='*60}")
        print(f"  Target: 0x{target_address:08X}")
        print(f"  Max depth: {max_depth}, Max offset: 0x{max_offset:X}")
        print(f"{'='*60}\n")
        
        STATIC_MIN = 0x00400000
        STATIC_MAX = 0x02000000
        
        regions = get_memory_regions()
        print(f"[*] Loaded {len(regions)} memory regions")
        
        # Build a map of all pointers in memory for faster lookup
        print("[*] Building pointer map (this may take a moment)...")
        pointer_map = {}  # value -> list of addresses that contain this value
        
        for base, size in regions:
            try:
                data = pm.read_bytes(base, min(size, 0x100000))  # Cap at 1MB per region
                for i in range(0, len(data) - 3, 4):
                    val = struct.unpack('<I', data[i:i+4])[0]
                    # Only track pointers that look like valid addresses
                    if 0x00100000 <= val <= 0x7FFFFFFF:
                        if val not in pointer_map:
                            pointer_map[val] = []
                        pointer_map[val].append(base + i)
            except:
                pass
        
        print(f"[*] Found {len(pointer_map)} unique pointer values\n")
        
        found_chains = []
        
        def search_recursive(addr, chain, depth):
            if depth > max_depth:
                return
            
            # Search for pointers to (addr - offset) for various offsets
            for offset in range(0, max_offset + 1, 4):
                search_addr = addr - offset
                if search_addr < 0x00100000:
                    continue
                    
                if search_addr in pointer_map:
                    for ptr_addr in pointer_map[search_addr]:
                        new_chain = [(ptr_addr, offset)] + chain
                        
                        # Check if we found a static pointer
                        if STATIC_MIN <= ptr_addr <= STATIC_MAX:
                            found_chains.append(new_chain)
                            # Print immediately
                            chain_str = f"[0x{ptr_addr:08X}]"
                            for p_addr, p_off in new_chain[1:]:
                                if p_off > 0:
                                    chain_str += f" + 0x{p_off:X}"
                                chain_str += f" -> [+0x{p_off:X}]" if p_off else ""
                            chain_str = f"0x{ptr_addr:08X}"
                            for _, p_off in new_chain:
                                chain_str += f" -> [+0x{p_off:X}]"
                            print(f"  [FOUND] {chain_str} = 0x{target_address:08X}")
                        else:
                            # Continue searching
                            search_recursive(ptr_addr, new_chain, depth + 1)
        
        print(f"[*] Searching for pointer chains to 0x{target_address:08X}...\n")
        search_recursive(target_address, [], 0)
        
        if not found_chains:
            print("\n[-] No pointer chains found to static memory.")
            print("    Try increasing max_offset or the target might use a different pattern.")
        else:
            print(f"\n[+] Found {len(found_chains)} pointer chain(s)!")
            print("\nTo use in code, read like this:")
            for i, chain in enumerate(found_chains[:5]):  # Show top 5
                print(f"\n  Chain {i+1}:")
                base_addr = chain[0][0]
                print(f"    base = 0x{base_addr:08X}")
                print(f"    addr = pm.read_int(base)")
                for j, (_, offset) in enumerate(chain):
                    if offset > 0:
                        print(f"    addr = pm.read_int(addr + 0x{offset:X})")
                print(f"    # addr should now point to 0x{target_address:08X}")
        
        return found_chains

    def interactive_scanner():
        """Interactive scanner mode"""
        print("\n" + "="*60)
        print("  Interactive Memory Scanner")
        print("="*60)
        print("""
Commands:
  si <value>       - Search for integer value
  sf <value>       - Search for float value  
  ss <text>        - Search for string
  d <address>      - Dump memory at address (hex)
  r <address>      - Read int at address (hex)
  rf <address>     - Read float at address (hex)
  rs <address>     - Read string at address (hex)
  n <value>        - Narrow down previous search (enter new value)
  p                - Probe around known pointers
  pc <address>     - Pointer chain scan (find static pointer to address)
  vc <address>     - Validate candidate pointer chain to address
  bf <base> <size> - Brute force scan struct (show all values in range)
  bfi <base> <val> - Find integer value in struct (search within 0x1000 bytes)
  bff <base> <val> - Find float value in struct
  bfs <base> <txt> - Find string in struct
  q                - Quit scanner
        """)
        
        last_results = []
        regions = None
        
        while True:
            try:
                cmd = input("\nscanner> ").strip()
            except EOFError:
                break
            
            if not cmd:
                continue
            
            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""
            
            if action == 'q':
                break
            
            elif action == 'si':
                try:
                    value = int(arg)
                    if regions is None:
                        regions = get_memory_regions()
                    last_results = search_int_value(value, regions)
                    if len(last_results) <= 20:
                        for addr in last_results:
                            print(f"  0x{addr:08X}")
                    else:
                        print(f"  (Showing first 20 of {len(last_results)})")
                        for addr in last_results[:20]:
                            print(f"  0x{addr:08X}")
                except ValueError:
                    print("[-] Invalid integer")
            
            elif action == 'sf':
                try:
                    value = float(arg)
                    if regions is None:
                        regions = get_memory_regions()
                    last_results = search_float_value(value, regions=regions)
                    if len(last_results) <= 20:
                        for addr in last_results:
                            print(f"  0x{addr:08X}")
                    else:
                        print(f"  (Showing first 20 of {len(last_results)})")
                        for addr in last_results[:20]:
                            print(f"  0x{addr:08X}")
                except ValueError:
                    print("[-] Invalid float")
            
            elif action == 'ss':
                if regions is None:
                    regions = get_memory_regions()
                last_results = search_string_value(arg, regions)
                if len(last_results) <= 20:
                    for addr in last_results:
                        print(f"  0x{addr:08X}")
                else:
                    print(f"  (Showing first 20 of {len(last_results)})")
                    for addr in last_results[:20]:
                        print(f"  0x{addr:08X}")
            
            elif action == 'd':
                try:
                    addr = int(arg, 16) if arg.startswith('0x') else int(arg, 16)
                    dump_memory(addr)
                except ValueError:
                    print("[-] Invalid address (use hex like 0x12345678)")
            
            elif action == 'r':
                try:
                    addr = int(arg, 16) if arg.startswith('0x') else int(arg, 16)
                    value = pm.read_int(addr)
                    print(f"  0x{addr:08X} = {value} (0x{value:X})" if value else f"  Failed to read")
                except Exception as e:
                    print(f"[-] Error: {e}")
            
            elif action == 'rf':
                try:
                    addr = int(arg, 16) if arg.startswith('0x') else int(arg, 16)
                    value = pm.read_float(addr)
                    print(f"  0x{addr:08X} = {value}" if value else f"  Failed to read")
                except Exception as e:
                    print(f"[-] Error: {e}")
            
            elif action == 'rs':
                try:
                    addr = int(arg, 16) if arg.startswith('0x') else int(arg, 16)
                    data = pm.read_bytes(addr, 100)
                    text = data.split(b'\x00')[0].decode('utf-8', errors='ignore')
                    print(f"  0x{addr:08X} = '{text}'")
                except Exception as e:
                    print(f"[-] Error: {e}")
            
            elif action == 'n':
                if not last_results:
                    print("[-] No previous results to narrow down")
                    continue
                try:
                    new_value = int(arg)
                    print(f"[*] Narrowing {len(last_results)} addresses to new value: {new_value}")
                    new_results = []
                    for addr in last_results:
                        try:
                            current = pm.read_int(addr)
                            if current == new_value:
                                new_results.append(addr)
                        except:
                            pass
                    last_results = new_results
                    print(f"[+] {len(last_results)} addresses remaining")
                    for addr in last_results[:20]:
                        print(f"  0x{addr:08X}")
                except ValueError:
                    print("[-] Invalid integer for narrowing")
            
            elif action == 'p':
                print("\n[*] Probing around known pointer bases...")
                known_bases = [
                    ("CLIENT+D450EC (main char)", 0x00400000 + 0x00D450EC),
                    ("CHAR_NAME", 0x011450EC),
                    ("DC_POINTER", 0x012CE35C),
                    ("TARGET_HP base", 0x012CE2E0),
                    ("TEAM_SIZE base", 0x0106D328),
                ]
                
                for name, base in known_bases:
                    results = probe_around_pointer(name, base, 0x100, "int")
                    if results:
                        print(f"  Found {len(results)} candidate values:")
                        for addr, val in results[:10]:
                            offset = addr - base
                            sign = "+" if offset >= 0 else ""
                            print(f"    0x{addr:08X} (base{sign}0x{offset:X}) = {val}")
            
            elif action == 'pc':
                try:
                    addr = int(arg, 16) if arg.startswith('0x') or any(c in arg for c in 'abcdefABCDEF') else int(arg, 16)
                    scan_pointer_chain(addr)
                except ValueError:
                    print("[-] Invalid address. Use hex like: pc 2DEA23C8")
            
            elif action == 'vc':
                # Verify chain: vc base_addr offset1 offset2 offset3 ...
                # Example: vc 0045BFB4 AD4 FEC C88 48 320
                try:
                    parts_vc = arg.split()
                    if len(parts_vc) < 2:
                        print("Usage: vc <base_addr> <offset1> <offset2> ...")
                        print("Example: vc 0045BFB4 AD4 FEC C88 48 320")
                        continue
                    
                    base_addr = int(parts_vc[0], 16)
                    offsets = [int(x, 16) for x in parts_vc[1:]]
                    
                    print(f"\n[*] Verifying pointer chain from 0x{base_addr:08X}")
                    print(f"    Offsets: {' -> '.join([f'+0x{o:X}' for o in offsets])}\n")
                    
                    addr = base_addr
                    print(f"  Step 0: [0x{addr:08X}]", end="")
                    value = pm.read_int(addr)
                    if value is None:
                        print(" = FAILED TO READ")
                        continue
                    print(f" = 0x{value:08X}")
                    addr = value
                    
                    # Follow all offsets EXCEPT the last one (which is the final offset to data)
                    for i, offset in enumerate(offsets[:-1]):
                        next_addr = addr + offset
                        print(f"  Step {i+1}: [0x{addr:08X} + 0x{offset:X}] = [0x{next_addr:08X}]", end="")
                        value = pm.read_int(next_addr)
                        if value is None:
                            print(" = FAILED TO READ")
                            break
                        print(f" = 0x{value:08X}")
                        addr = value
                    
                    # Apply the last offset without dereferencing
                    final_offset = offsets[-1]
                    final_addr = addr + final_offset
                    print(f"  Step {len(offsets)}: 0x{addr:08X} + 0x{final_offset:X} = 0x{final_addr:08X} (final data address)")
                    
                    print(f"\n  Final address: 0x{final_addr:08X}")
                    print(f"\n  Reading values at final address:")
                    try:
                        print(f"    +0x000 (Max HP?):    {pm.read_int(final_addr + 0x000)}")
                    except:
                        print(f"    +0x000 (Max HP?):    Failed to read")
                    try:
                        print(f"    +0x004 (Max Mana?):  {pm.read_int(final_addr + 0x004)}")
                    except:
                        print(f"    +0x004 (Max Mana?):  Failed to read")
                    try:
                        print(f"    +0x360 (Cur HP?):    {pm.read_int(final_addr + 0x360)}")
                    except:
                        print(f"    +0x360 (Cur HP?):    Failed to read")
                    try:
                        print(f"    +0x364 (Cur Mana?):  {pm.read_int(final_addr + 0x364)}")
                    except:
                        print(f"    +0x364 (Cur Mana?):  Failed to read")
                    try:
                        name_bytes = pm.read_bytes(final_addr + 0x064, 20)
                        name = name_bytes.split(b'\x00')[0].decode('utf-8', errors='ignore')
                        print(f"    +0x064 (Name?):      '{name}'")
                    except:
                        print(f"    +0x064 (Name?):      Failed to read")
                        
                except ValueError as e:
                    print(f"[-] Invalid input: {e}")
                    print("Usage: vc <base_addr> <offset1> <offset2> ...")
                    print("Example: vc 0045BFB4 AD4 FEC C88 48 320")
            
            elif action == 'bf':
                # Brute force dump - show all values in struct
                # Usage: bf <base_address> [size_in_bytes]
                try:
                    parts_bf = arg.split()
                    base_addr = int(parts_bf[0], 16)
                    size = int(parts_bf[1], 16) if len(parts_bf) > 1 else 0x400
                    
                    print(f"\n[*] Brute force scanning struct at 0x{base_addr:08X}, size 0x{size:X}")
                    print(f"{'Offset':<10} {'Int':<15} {'Float':<15} {'Hex':<12} {'Bytes'}")
                    print("-" * 70)
                    
                    for offset in range(0, size, 4):
                        addr = base_addr + offset
                        try:
                            int_val = pm.read_int(addr)
                            float_val = pm.read_float(addr)
                            raw_bytes = pm.read_bytes(addr, 4)
                            hex_val = f"0x{int_val & 0xFFFFFFFF:08X}" if int_val else "N/A"
                            
                            # Skip zeros for cleaner output
                            if int_val == 0:
                                continue
                            
                            # Check if float is reasonable
                            float_str = "N/A"
                            if float_val and -1000000 < float_val < 1000000 and float_val != 0:
                                float_str = f"{float_val:.2f}"
                            
                            # Show ASCII if printable
                            ascii_str = ""
                            for b in raw_bytes:
                                if 32 <= b < 127:
                                    ascii_str += chr(b)
                                else:
                                    ascii_str += "."
                            
                            print(f"+0x{offset:03X}     {int_val:<15} {float_str:<15} {hex_val:<12} {ascii_str}")
                        except:
                            pass
                            
                except ValueError as e:
                    print(f"[-] Invalid input: {e}")
                    print("Usage: bf <base_addr> [size]")
                    print("Example: bf 2DEA23C8 400")
            
            elif action == 'bfi':
                # Brute force find integer in struct
                # Usage: bfi <base_address> <value_to_find>
                try:
                    parts_bf = arg.split()
                    if len(parts_bf) < 2:
                        print("Usage: bfi <base_addr> <int_value>")
                        print("Example: bfi 2DEA23C8 150   # Find level 150")
                        continue
                    
                    base_addr = int(parts_bf[0], 16)
                    search_val = int(parts_bf[1])
                    search_range = 0x1000  # Search within 4KB
                    
                    print(f"\n[*] Searching for integer {search_val} in struct at 0x{base_addr:08X}")
                    found = []
                    
                    for offset in range(0, search_range, 4):
                        addr = base_addr + offset
                        try:
                            val = pm.read_int(addr)
                            if val == search_val:
                                found.append(offset)
                                print(f"  [FOUND] +0x{offset:03X} (0x{addr:08X}) = {val}")
                        except:
                            pass
                    
                    # Also check 2-byte values (shorts)
                    for offset in range(0, search_range, 2):
                        addr = base_addr + offset
                        try:
                            val = pm.read_short(addr)
                            if val == search_val and offset not in found:
                                print(f"  [FOUND SHORT] +0x{offset:03X} (0x{addr:08X}) = {val}")
                        except:
                            pass
                    
                    # Check single bytes for small values
                    if search_val < 256:
                        for offset in range(0, search_range):
                            addr = base_addr + offset
                            try:
                                val = pm.read_bytes(addr, 1)[0]
                                if val == search_val:
                                    print(f"  [FOUND BYTE] +0x{offset:03X} (0x{addr:08X}) = {val}")
                            except:
                                pass
                    
                    if not found:
                        print("  No matches found as 4-byte int in first 0x1000 bytes")
                        
                except ValueError as e:
                    print(f"[-] Invalid input: {e}")
                    print("Usage: bfi <base_addr> <int_value>")
            
            elif action == 'bff':
                # Brute force find float in struct
                try:
                    parts_bf = arg.split()
                    if len(parts_bf) < 2:
                        print("Usage: bff <base_addr> <float_value>")
                        print("Example: bff 2DEA23C8 123.5   # Find position 123.5")
                        continue
                    
                    base_addr = int(parts_bf[0], 16)
                    search_val = float(parts_bf[1])
                    tolerance = 0.01  # Allow small difference
                    search_range = 0x1000
                    
                    print(f"\n[*] Searching for float ~{search_val} in struct at 0x{base_addr:08X}")
                    
                    for offset in range(0, search_range, 4):
                        addr = base_addr + offset
                        try:
                            val = pm.read_float(addr)
                            if val and abs(val - search_val) < tolerance:
                                print(f"  [FOUND] +0x{offset:03X} (0x{addr:08X}) = {val}")
                        except:
                            pass
                            
                except ValueError as e:
                    print(f"[-] Invalid input: {e}")
                    print("Usage: bff <base_addr> <float_value>")
            
            elif action == 'bfs':
                # Brute force find string in struct
                try:
                    parts_bf = arg.split(maxsplit=1)
                    if len(parts_bf) < 2:
                        print("Usage: bfs <base_addr> <string>")
                        print("Example: bfs 2DEA23C8 CJSpace")
                        continue
                    
                    base_addr = int(parts_bf[0], 16)
                    search_str = parts_bf[1].encode('utf-8')
                    search_range = 0x1000
                    
                    print(f"\n[*] Searching for '{parts_bf[1]}' in struct at 0x{base_addr:08X}")
                    
                    try:
                        data = pm.read_bytes(base_addr, search_range)
                        pos = 0
                        while True:
                            idx = data.find(search_str, pos)
                            if idx == -1:
                                break
                            print(f"  [FOUND] +0x{idx:03X} (0x{base_addr + idx:08X})")
                            pos = idx + 1
                    except Exception as e:
                        print(f"[-] Error reading memory: {e}")
                        
                except ValueError as e:
                    print(f"[-] Invalid input: {e}")
                    print("Usage: bfs <base_addr> <string>")
            
            else:
                print("[-] Unknown command. Type 'q' to quit.")
    
    # ==================== MAIN LOGIC ====================
    
    # Try to create Pointers instance for display_info
    try:
        p = Pointers(args.pid)
    except:
        p = None
    
    def safe_call(func, default="N/A"):
        """Safely call a function and return default on error"""
        try:
            result = func()
            return result if result is not None else default
        except Exception as e:
            return f"Error: {e}"

    def display_info():
        print(f"\n{'='*60}")
        print(f"  Character Information")
        print(f"{'='*60}")
        print(f"  Name:          {safe_call(p.get_char_name)}")
        print(f"  Level:         {safe_call(p.get_level)}")
        #print(f"  HP:            {safe_call(p.get_hp)} / {safe_call(p.get_max_hp)}")
        #print(f"  Mana:          {safe_call(p.get_mana)} / {safe_call(p.get_max_mana)}")
        #print(f"  Gold:          {safe_call(p.get_gold)}")
        print(f"  Position:      X={safe_call(p.get_x)}, Y={safe_call(p.get_y)}")
        #print(f"  Location:      {safe_call(p.get_location)}")

        print(f"\n{'='*60}")
        print(f"  Status")
        print(f"{'='*60}")
        print(f"  In Battle:     {safe_call(p.is_in_battle)}")
        #print(f"  Sitting:       {safe_call(p.is_sitting)}")
        print(f"  Mount:         {safe_call(p.mount)}")
        print(f"  Bag Open:      {safe_call(p.is_bag_open)}")
        #print(f"  DC:            {safe_call(p.get_dc)}")
        #print(f"  System Menu:   {safe_call(p.get_system_menu)}")
        #print(f"  Confirm Box:   {safe_call(p.confirm_box)}")
        #print(f"  Dialog:        {safe_call(p.get_dialog)}")
        #print(f"  Notification:  {safe_call(p.get_notification)}")
        #print(f"  Loot Window:   {safe_call(p.loot_window)}")

        print(f"\n{'='*60}")
        print(f"  Target Information")
        print(f"{'='*60}")
        print(f"  Selected:      {safe_call(p.is_target_selected)}")
        print(f"  Target Name:   {safe_call(p.get_target_name)}")
        print(f"  Target HP:     {safe_call(p.target_hp)}")
        #print(f"  Teammate HP:   {safe_call(p.get_teammate_hp)}")
        #print(f"  Target Dead:   {safe_call(p.is_target_dead)}")
        #print(f"  Target ID:     {safe_call(p.get_target_id)}")

        print(f"\n{'='*60}")
        print(f"  Team Information")
        print(f"{'='*60}")
        print(f"  Team Size:     {safe_call(p.get_team_size)}")
        print(f"  Member 1:      {safe_call(p.team_name_1)}")
        print(f"  Member 2:      {safe_call(p.team_name_2)}")
        print(f"  Member 3:      {safe_call(p.team_name_3)}")
        print(f"  Member 4:      {safe_call(p.team_name_4)}")

        print(f"\n{'='*60}")
        print(f"  Inventory")
        print(f"{'='*60}")
        print(f"  Bag Slot 1:    {safe_call(p.bag_1_quantity)}")
        print(f"  Bag Slot 2:    {safe_call(p.bag_2_quantity)}")

        print(f"\n{'='*60}")
        name = p.get_char_name()
        print(f"CHAR_NAME: {name}")
        level = p.get_level()
        print(f"LEVEL: {level}")
        '''
        team_name_1 = p.team_name_1()
        print(f"TEAM_NAME_1: {team_name_1}")
        team_name_2 = p.team_name_2()
        print(f"TEAM_NAME_2: {team_name_2}")
        team_name_3 = p.team_name_3()
        print(f"TEAM_NAME_3: {team_name_3}")
        team_name_4 = p.team_name_4()
        print(f"TEAM_NAME_4: {team_name_4}")
        
        hp = p.target_hp()
        print(f"TARGET_HP: {hp}")
        target_name = p.get_target_name()
        print(f"TARGET_NAME: {target_name}")
        get_hp = p.get_hp()
        print(f"CHAR_HP : {get_hp}")
        hp_plus = p.get_hp_plus()
        print(f"CHAR_HP_PLUS : {hp_plus}")
        hp_buff = p.get_hp_buff()
        print(f"CHAR_HP_BUFF : {hp_buff}")
        max_hp = p.get_max_hp()
        print(f"CHAR_MAX_HP : {max_hp}")
        battle = p.is_in_battle()
        print(f"CHAR_BATTLE_STATUS : {battle}")
        mana = p.get_mana()
        print(f"CHAR_MANA : {mana}")
        mana_buff = p.get_mana_buff()
        print(f"CHAR_MANA_BUFF : {mana_buff}")
        max_mana = p.get_max_mana()
        print(f"CHAR_MAX_MANA : {max_mana}")
        sit = p.is_sitting()
        print(f"CHAR_SIT : {sit}")
        x_pos = p.get_x()
        print(f"CHAR_X_POS : {x_pos}")
        y_pos = p.get_y()
        print(f"CHAR_Y_POS : {y_pos}")
        bag_open = p.is_bag_open()
        print(f"CHAR_BAG_OPEN : {bag_open}")
        team_size = p.get_team_size()
        print(f"TEAM_SIZE : {team_size}")
        print(f"mounted : {p.mount()}")
        t_ptr = p.search_id()
        print(f"search_id : {t_ptr}")
        '''
        print()

    # Handle different modes
    if args.scan:
        interactive_scanner()
    
    elif args.search_int is not None:
        results = search_int_value(args.search_int)
        print("\nResults (showing up to 50):")
        for addr in results[:50]:
            print(f"  0x{addr:08X}")
        if len(results) > 50:
            print(f"  ... and {len(results) - 50} more")
    
    elif args.search_float is not None:
        results = search_float_value(args.search_float)
        print("\nResults (showing up to 50):")
        for addr in results[:50]:
            print(f"  0x{addr:08X}")
        if len(results) > 50:
            print(f"  ... and {len(results) - 50} more")
    
    elif args.search_string:
        results = search_string_value(args.search_string)
        print("\nResults (showing up to 50):")
        for addr in results[:50]:
            print(f"  0x{addr:08X}")
        if len(results) > 50:
            print(f"  ... and {len(results) - 50} more")
    
    elif args.dump:
        try:
            addr = int(args.dump, 16) if args.dump.startswith('0x') else int(args.dump, 16)
            dump_memory(addr, args.dump_size)
        except ValueError:
            print("[-] Invalid address format. Use hex like 0x12CE35C")
    
    elif args.probe:
        print("\n[*] Probing around known pointer bases...")
        print(f"[*] Range: ±0x{args.probe_range:X} bytes\n")
        
        known_bases = [
            ("CLIENT+D450EC (main char base)", 0x00400000 + 0x00D450EC),
            ("CHAR_NAME_POINTER", 0x011450EC),
            ("DC_POINTER", 0x012CE35C),
            ("TARGET base", 0x012CE2E0),
            ("TEAM_SIZE base", 0x0106D328),
            ("ZOOM base", 0x116FFF4),
            ("NOTIFICATION", 0x0117097C),
        ]
        
        for name, base in known_bases:
            print(f"\n{'='*60}")
            print(f"  {name} (0x{base:08X})")
            print(f"{'='*60}")
            
            # Look for integers
            results = probe_around_pointer(name, base, args.probe_range, "int")
            if results:
                print(f"\n  Candidate integers ({len(results)} found, showing top 15):")
                for addr, val in results[:15]:
                    offset = addr - base
                    sign = "+" if offset >= 0 else ""
                    print(f"    0x{addr:08X} (base{sign}0x{offset:X}) = {val}")
            
            # Look for strings
            str_results = probe_around_pointer(name, base, args.probe_range, "string")
            if str_results:
                print(f"\n  Candidate strings ({len(str_results)} found, showing top 10):")
                for addr, val in str_results[:10]:
                    offset = addr - base
                    sign = "+" if offset >= 0 else ""
                    print(f"    0x{addr:08X} (base{sign}0x{offset:X}) = '{val}'")
    
    elif args.loop:
        if p is None:
            print("[-] Cannot use loop mode - Pointers class failed to initialize")
            sys.exit(1)
        print("[*] Continuous monitoring mode (Ctrl+C to stop)\n")
        try:
            while True:
                # Clear screen on Windows
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                display_info()
                print(f"\n[Refreshing every {args.interval}s - Press Ctrl+C to stop]")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[*] Monitoring stopped.")
    
    else:
        if p is not None:
            display_info()
        else:
            print("[-] Pointers class failed to initialize. Use --scan for interactive scanner.")
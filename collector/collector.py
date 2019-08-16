

def validate(irr_text):
    if len(irr_text) > 10:
        lines = irr_text.split('\n')
        for line in lines:
            if len(line) > 5:
                if not line.startswith("remarks:"):
                    if line.startswith('%ERROR:201'):
                        return False
                    elif line.startswith("as-block:"):
                        block = line.split()
                        if len(block) < 4:
                            continue
                        else:
                            try:
                                end_of_block = int(block[-1].lstrip('AS'))
                            except ValueError:
                                print("Invalid block value.")
                            
            elif


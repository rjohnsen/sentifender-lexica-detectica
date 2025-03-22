class Markdown:
    @staticmethod
    def renderTable(rows: list) -> str:
        stringbuilder = []

        # Setup up headers
        stringbuilder.append(f'| {" | ".join(rows[0].keys())} |')
        stringbuilder.append("| --- " * len(rows[0].keys()))

        # Handling rows
        for row in rows:
            stringbuilder.append(f'| {" | ".join(row.values())} |')

        return "\n".join(stringbuilder)
    
    @staticmethod
    def renderList(data: list) -> str:
        return "\n".join(["- {0}".format(i) for i in data])
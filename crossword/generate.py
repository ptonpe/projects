import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        #deep copy
        domain_copy = copy.deepcopy(self.domains)

        #iterate through copy
        for variable in domain_copy:
            length = variable.length

            #iterate through words
            for word in domain_copy[variable]:
                if len(word) != length:
                    #if length doesn't fit variable, remove it from domain
                    self.domains[variable].remove(word)



    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        #get overlapping cells
        xoverlap, yoverlap = self.crossword.overlaps[x,y]

        revision_made = False

        #domain copy
        domains_copy = copy.deepcopy(self.domains)

        #overlap occurs
        if xoverlap:
            #iterate through words in x domain
            for xword in domains_copy[x]:
                matched_value = False
                #iterate through words in y domain
                for yword in self.domains[y]:
                    #if x and y word have same letter in overlapping position
                    if xword[xoverlap] == yword[yoverlap]:
                        matched_value = True
                        break
                if matched_value:
                    #continue to new x if match occurred
                    continue
                else:
                    #remove word from domain bc no match x-y word
                    self.domains[x].remove(xword)
                    revision_made = True

        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if not arcs:
            #no arcs given, start with initial queue
            queue = []

            #populate queue
            for var1 in self.domains:
                for var2 in self.crossword.neighbors(var1):
                    if self.crossword.overlaps[var1, var2] is not None:
                        queue.append((var1, var2))

        while len(queue) > 0:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False

                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))
            return True




    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for variable in self.domains:
            if variable not in assignment:
                return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        #distinct values, correct length, no conflicts
        words = [*assignment.values()]
        if len(words) != len(set(words)):
            return False


        #check for length
        for variable in assignment:
            if variable.length != len(assignment[variable]):
                return False

        #check for conflicts with neighbors
        for variable in assignment:
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    x, y = self.crossword.overlaps[variable, neighbor]
                    if assignment[variable][x] != assignment[neighbor][y]:
                        return False

        #everything consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        #make temp dict
        word_dict = {}

        #get neighbors
        neighbors = self.crossword.neighbors(var)

        #iterate through var words
        for word in self.domains[var]:
            eliminated = 0

            for neighbor in neighbors:
                #do not count if neighbor has assigned value
                if neighbor in assignment:
                    continue

                else:
                    #calc overlap bw two variables
                    xoverlap, yoverlap = self.crossword.overlaps[var, neighbor]
                    for neighbor_word in self.domains[neighbor]:
                        #iterate through neighbor words, check for eliminated
                        if word[xoverlap] != neighbor_word[yoverlap]:
                            eliminated += 1

            word_dict[word] = eliminated

        #sort var dictionary by # of eliminated neighbor values
        sorted_dict = {k: v for k, v in sorted(word_dict.items(), key = lambda item: item[1])}

        return[*sorted_dict]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        choice_dict = {}

        #iterate through vars in domains
        for variable in self.domains:
            if variable not in assignment:
                #if var not in assignment, add to temp dict
                choice_dict[variable] = self.domains[variable]

        sorted_list = [v for v, k in sorted(choice_dict.items(), key=lambda item: len(item[1]))]

        return sorted_list[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        #if assignment already ready
        if len(assignment) == len(self.domains):
            return assignment

        #selecting one from unassigned variables
        variable = self.select_unassigned_variable(assignment)

        #iterate words in that var
        for value in self.domains[variable]:
            #assignment copy with updated var value
            assignment_copy = assignment.copy()
            assignment_copy[variable] = value

            #check for consistency
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

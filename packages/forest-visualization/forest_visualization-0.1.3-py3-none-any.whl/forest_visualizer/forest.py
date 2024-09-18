#from turtle import *
from PIL import Image, ImageDraw, ImageFont

class Forest:
    def __init__(self):
        self.info = []
        self.noofchildren = []
        self.i = 0
        self.j = 0  # Index for drawing nodes

    


    def insert(self, NodeName, ParentName):
        if ParentName == 'N/A' and len(self.noofchildren) == 0:
            self.info.insert(0, NodeName)
            self.noofchildren.insert(0, 1)
            self.noofchildren.insert(1, 0)
            self.i += 1
        elif ParentName == 'N/A':
            self.info.insert(0, NodeName)
            self.noofchildren[0] += 1
            self.noofchildren.insert(1, 0)
            self.i += 1
        else:
            # Finding the parent's index
            if ParentName in self.info:
                PIndex = self.info.index(ParentName)
            else:
                PIndex = -1
                print(f"Parent Node '{ParentName}' does not exist")

            # Finding insertion position and performing insertion
            if PIndex >= 0:
                Sum = sum(self.noofchildren[0:PIndex + 1])
                self.info.insert(Sum, NodeName)
                self.noofchildren[PIndex + 1] += 1
                self.noofchildren.insert(Sum + 1, 0)

    def level_traversal(self):
        T = ''
        n = len(self.info)  # Total number of nodes
        Left = 0
        Right = 0
        PosInfo = 0  # Start with index 1 because root is already processed in the first row

        while PosInfo < n:
            TotalChild = 0
            for PosChild in range(Left, Right + 1):
                for i in range(self.noofchildren[PosChild]):
                    if PosInfo < n:  # Ensure index is within bounds
                        T += self.info[PosInfo]+','
                        PosInfo += 1
                    else:
                        break  # Prevent out of bounds error
                if PosChild < Right:
                    T += "*"
                TotalChild += self.noofchildren[PosChild]
            Left = Right + 1
            Right = Right + TotalChild
            T += "\n"

        print(T.rstrip())  # Print traversal result
    def find_parent(self, NodeName):
        if NodeName not in self.info:
            print(f"Node '{NodeName}' not found")
            return None

        DeletionElement = NodeName
        k = self.info.index(DeletionElement) + 1
        i = 0
        Sum = 0

        # Loop to find the parent's index
        while Sum < k:
            Sum = Sum + self.noofchildren[i]
            i = i + 1

        # Parent's index is `i-2` because `i` overshoots by 1 during the last increment
        RootParent = i - 2
        if RootParent >= 0:
            return self.info[RootParent]
        else:
            return None  # Return None if there's no parent (e.g., root node)
    def post_order_traversal(self, element):
        if element not in self.info:
            print(f"Node '{element}' not found in the forest.")
            return None

        Post = []
        Path = []
        NoChild = []
        Index = []

        def left_traverse(node):
            k = self.info.index(node) + 1
            s = sum(self.noofchildren[0:k])

            Path.append(self.info[k - 1])
            NoChild.append(self.noofchildren[k])
            Index.append(k)

            while self.noofchildren[k] != 0:
                k1 = k
                k = s + 1
                s = s + sum(self.noofchildren[k1:k])
                Path.append(self.info[k - 1])
                NoChild.append(self.noofchildren[k])
                Index.append(k)

        # Traverse the left subtree
        left_traverse(element)

        # Process the nodes in post-order
        while len(Path) > 0:
            Post.append(Path[-1])
            NextIndex = Index[-1]
            NoChild.pop(-1)
            Path.pop(-1)
            Index.pop(-1)

            if len(NoChild) > 0:
                NoChild[-1] -= 1

                if NoChild[-1] != 0:
                    left_traverse(self.info[NextIndex])

        return Post


    def display(self):
        print("Info:", self.info)
        print("No of children:", self.noofchildren)
    def find_path_to_root(self, NodeName):
        if NodeName not in self.info:
            print(f"Node '{NodeName}' not found")
            return None

        Path = []
        k = self.info.index(NodeName) + 1
        RootParent = self.info.index(NodeName)

        while RootParent >= 0:
            i = 0
            Sum = 0
            Path.insert(0, self.info[RootParent])  # Insert at the beginning to build the path from root
            while Sum < k:
                Sum += self.noofchildren[i]
                i += 1
            RootParent = i - 2  # Find the next parent
            k = RootParent + 1

        return Path
    def delete_node(self, DeletionElement):
        if DeletionElement not in self.info:
            print(f"Node '{DeletionElement}' not found")
            return

        i = 0
        Sum = 0
        k = self.info.index(DeletionElement) + 1
        while Sum < k:
            Sum += self.noofchildren[i]
            i += 1
        RootParent = i - 2
        k = k - 1

        StackValue = []
        StackNoofchildren = []
        StackIndex = []
        StackValue.append(self.info[k])
        StackNoofchildren.append(self.noofchildren[k + 1])
        StackIndex.append(k)

        Sum = sum(StackNoofchildren)

        i = 0
        while len(StackValue) < Sum + 1:
            endIndex = sum(self.noofchildren[0:StackIndex[i] + 2])
            startIndex = endIndex - self.noofchildren[StackIndex[i] + 1]
            for k in range(startIndex, endIndex):
                StackValue.append(self.info[k])
                StackNoofchildren.append(self.noofchildren[k + 1])
                StackIndex.append(k)
            Sum = sum(StackNoofchildren)
            i += 1

        Parent = []
        j = 0
        Parent.append(RootParent)
        for i in range(0, len(StackValue)):
            for k in range(0, StackNoofchildren[i]):
                Parent.append(StackIndex[i])

        for i in range(len(StackValue) - 1, -1, -1):
            k = self.info.index(StackValue[i])
            del self.info[k]
            del self.noofchildren[k + 1]
            if Parent[i] >= 0 and i != 0:
                self.info.insert(Parent[i] + 1, StackValue[i])
                self.noofchildren.insert(Parent[i] + 2, StackNoofchildren[i])

        self.noofchildren[RootParent + 1] = self.noofchildren[RootParent + 1] + StackNoofchildren[0] - 1
    def pre_order_traversal(self, element):
        if element not in self.info:
            print(f"Node '{element}' not found in the forest.")
            return None

        Path = []
        NoChild = []
        Index = []

        def left_traverse(node):
            k = self.info.index(node) + 1
            s = sum(self.noofchildren[0:k])

            Path.append(self.info[k - 1])
            if self.noofchildren[k] > 0:
                NoChild.append(self.noofchildren[k] - 1)
            else:
                NoChild.append(self.noofchildren[k])

            Index.append(k)

            while self.noofchildren[k] != 0:
                k1 = k
                k = s + 1
                s = s + sum(self.noofchildren[k1:k])
                Path.append(self.info[k - 1])
                if self.noofchildren[k] > 0:
                    NoChild.append(self.noofchildren[k] - 1)
                else:
                    NoChild.append(self.noofchildren[k])
                Index.append(k)

        # Start pre-order traversal
        left_traverse(element)

        # Process the nodes in pre-order
        while sum(NoChild) > 0:
            i = len(NoChild) - 1
            while i >= 0:
                i = i - 1
                if NoChild[i] != 0:
                    break

            I1 = Index[i + 1] + self.noofchildren[Index[i]] - NoChild[i]
            NoChild[i] = NoChild[i] - 1
            left_traverse(self.info[I1 - 1])

        return Path


    # Function to draw the tree using turtle graphics
    def draw_tree(self, size_x=700, size_y=400, radius=30, gap=30):
        InputTree = self.noofchildren
        Info = self.info
        XCordinate = [0] * len(InputTree)

        # Turtle setup
        #setup(size_x, size_y)
        self.radius = radius
        self.gap = gap
        SizeX=size_x
        SizeY=size_y

        image = Image.new('RGB', (SizeX, SizeY), 'white')
        draw = ImageDraw.Draw(image)

        def draw_circle(draw, center_x, center_y, radius, text='', outline_color='blue', fill_color=None, text_color='black', line_width=1, font_size=20):
            # Calculate the bounding box using the center and radius
            top_left = (center_x - radius, center_y - radius)
            bottom_right = (center_x + radius, center_y + radius)

            # Draw the circle
            draw.ellipse([top_left, bottom_right], outline=outline_color, fill=fill_color, width=line_width)

            if text:
                # Load a font
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = ImageFont.load_default()

                # Calculate text size and position
                text_width, text_height = draw.textsize(text, font=font)
                text_x = center_x - (text_width / 2)
                text_y = center_y - (text_height / 2)

                # Draw the text
                draw.text((text_x, text_y), text, fill=text_color, font=font)
           
        def draw_node(X, height, N, Cx, Cy):
            Init = self.j
            if N != 0:
                Distance = X[1] - X[0]
                BlockDistance = Distance / N
                XCenter = X[0] + (BlockDistance / 2)
                XStart = X[0]
                XEnd = X[0] + BlockDistance
                for i in range(0, N):
                    self.j += 1
                    #up()
                    #goto(XCenter, height - radius)
                    draw_circle(draw, center_x=XCenter+(SizeX/2), center_y=SizeY/2-(height), radius=radius, outline_color='red',text=Info[self.j - 1])
                    #down()
                    #circle(radius)
                    if Init != 0:
                        #up()
                        #goto(Cx, Cy)
                        #down()
                        #goto(XCenter, height + radius)
                        start = (Cx+(SizeX/2),SizeY/2-Cy)
                        end = (XCenter+(SizeX/2), SizeY/2-(height+radius))
                        draw.line([start, end], fill='black', width=1)
                    #up()
                    #goto(XCenter, height - radius / 4)
                    #down()
                    #write(Info[self.j - 1], align="center", font=("Arial", 16, "bold"))
                    XCordinate[self.j] = [[XStart, XEnd], XCenter, height - radius]
                    XStart = XEnd
                    XEnd += BlockDistance
                    XCenter += BlockDistance

        y = size_y / 2
        X = [0] * 2
        height = y - (radius * 2)
        X[0] = size_x / 2 * -1
        X[1] = size_x / 2
        Cx, Cy = 0, y
        XCordinate[0] = [X, Cx, Cy]
        height -= gap
        for i in range(0, len(InputTree)):
            N = InputTree[i]
            draw_node(XCordinate[i][0], XCordinate[i][2] - radius - gap, N, XCordinate[i][1], XCordinate[i][2])
        #getscreen()._root.mainloop()
        image.save('two_circles.png')
        image.show()
        self.j = 0  # Index for drawing nodes
#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# C Deverell
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts splits all nodes in the model

#------------------------------------------------------------
# DISCLAIMER
#------------------------------------------------------------
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

scenario = target


nodeType = model.getType('GKNode')

splitnodecmd = GKSplitNodeCmd()


nodes = model.getCatalog().getObjectsByType(nodeType).values()

splitnodecmd.setData(nodes)

model.getCommander().addCommand(splitnodecmd)


print("Finished Splitting Nodes")
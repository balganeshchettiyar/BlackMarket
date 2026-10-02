class TeamService {
    static getCurrentTeam() {
        return localStorage.getItem('currentTeamId') || 'TEAM_07';
    }

    static setCurrentTeam(teamId) {
        localStorage.setItem('currentTeamId', teamId);
    }

    static async getTeamState(teamId) {
        const stateStr = localStorage.getItem(`blackMarketState_${teamId}`);
        if (stateStr) {
            try {
                const parsed = JSON.parse(stateStr);
                if (parsed && typeof parsed === 'object') {
                    // Check version or migrate if needed
                    if (!parsed.version) {
                        parsed.version = 1;
                    }
                    if (!parsed.puzzleProgress) {
                        parsed.puzzleProgress = { cluesFound: [], riddleSolved: false, finalCodeEntered: false };
                    }
                    if (!parsed.teamName) {
                        parsed.teamName = `Team ${teamId.replace('TEAM_', '')}`;
                    }
                    if (parsed.codeAttempts === undefined) {
                        parsed.codeAttempts = 0;
                    }
                    if (parsed.money === undefined) {
                        parsed.money = BLACK_MARKET_CONFIG.initialTeamMoney;
                    }
                    return parsed;
                }
            } catch (error) {
                console.error("[BLACK MARKET] Failed to load saved state", error);
                // Fall through to initialize new state safely
            }
        }
        
        // Initialize new team state
        const newState = {
            version: 1,
            teamId: teamId,
            teamName: `Team ${teamId.replace('TEAM_', '')}`,
            money: BLACK_MARKET_CONFIG.initialTeamMoney,
            blackMarketUnlocked: false,
            codeAttempts: 0,
            inventory: { hints: [], buffs: [], mystery: [] },
            purchasedItems: [],
            transactions: [],
            puzzleProgress: { cluesFound: [], riddleSolved: false, finalCodeEntered: false }
        };
        await this.saveTeamState(teamId, newState);
        return newState;
    }

    static async saveTeamState(teamId, state) {
        localStorage.setItem(`blackMarketState_${teamId}`, JSON.stringify(state));
    }

    static async getBalance(teamId) {
        const state = await this.getTeamState(teamId);
        return state.money;
    }

    static getItemPrice(team, item) {
        // Future dynamic pricing goes here
        return item.price;
    }

    static async deductFunds(teamId, amount) {
        const state = await this.getTeamState(teamId);
        if (state.money < amount) throw new Error("INSUFFICIENT FUNDS");
        state.money -= amount;
        await this.saveTeamState(teamId, state);
        return state.money;
    }

    static async purchaseItem(teamId, category, itemId) {
        const state = await this.getTeamState(teamId);
        
        const categoryItems = BLACK_MARKET_CONFIG.items[category];
        const item = categoryItems.find(i => i.id === itemId);
        if (!item) throw new Error("ITEM NOT FOUND");

        const effectivePrice = this.getItemPrice(state, item);

        // Check purchase limits
        const ownedCount = state.purchasedItems.filter(id => id === itemId).length;
        if (item.maxPurchases && ownedCount >= item.maxPurchases) {
            throw new Error("ALREADY ACQUIRED");
        }

        if (state.money < effectivePrice) {
            throw new Error("INSUFFICIENT FUNDS");
        }

        // Deduct money and add to inventory
        state.money -= effectivePrice;
        state.purchasedItems.push(itemId);

        const timestamp = new Date().toISOString();
        const txnId = `TXN_${Math.random().toString(36).substr(2, 6).toUpperCase()}`;

        state.transactions.push({
            id: txnId,
            itemId: itemId,
            category: category,
            price: effectivePrice,
            timestamp: timestamp,
            balanceAfter: state.money
        });

        state.inventory[category].push({
            itemId: itemId,
            purchasedAt: timestamp,
            revealed: false // for hints/mystery
        });

        await this.saveTeamState(teamId, state);
        
        return { 
            success: true, 
            newBalance: state.money, 
            transaction: txnId,
            effectivePrice: effectivePrice
        };
    }

    static async unlockBlackMarket(teamId) {
        const state = await this.getTeamState(teamId);
        state.blackMarketUnlocked = true;
        await this.saveTeamState(teamId, state);
    }

    static async recordCodeAttempt(teamId) {
        const state = await this.getTeamState(teamId);
        state.codeAttempts++;
        await this.saveTeamState(teamId, state);
        return state.codeAttempts;
    }

    static async revealItem(teamId, category, itemId) {
        const state = await this.getTeamState(teamId);
        const invItem = state.inventory[category].find(i => i.itemId === itemId);
        if (invItem) {
            invItem.revealed = true;
            await this.saveTeamState(teamId, state);
        }
    }
}

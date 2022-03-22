// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.5.17 || ^0.6.2 || ^0.7.0 || ^0.8.0;

contract TestFreeze {

    /**
     * @dev Contract can accept value while creating.
     */
    constructor() public payable {}

    /**
     * @dev Freeze `amount` balance of contract to get resource for `receiver`
     * which type is `res` (0 for bandwidth, 1 for energy).
     *
     * Below situations can cause `revert` excepiton:
     * 1. `amount` is greater than long.max_value or contract balance.
     * 2. `amount` is less than 10e6 sun (1 trx).
     * 3. `res` is not zero or one.
     * 4. `receiver` is contract address (exclude this contract).
     *
     * Caution:
     * 1. Balance freezing is also at least three days.
     * 2. Contract can never use its bandwidth or energy.
     * 3. If `receiver` account does not exist, the operation will create it.
     * 4. If contract still has delegated frozen balance for other account,
     *    suicide can not be excuted and throw a revert exception.
     */
    function freezeBalance(address payable receiver, uint amount, uint res) payable external {
        receiver.freeze(amount, res);
    }

    /**
     * @dev Unfreeze specific balance to get corresponding balance.You can use
     * `receiver' and 'res'  (0 for bandwidth, 1 for energy) parameters to
     * unfreeze specific balance.
     *
     * Below situations can cause `revert` excepiton:
     * 1. `res` is not zero or one.
     * 2. Frozen relationship between contract and `receiver` does not exist.
     * 3. It is not time to unfreeze the specific balance.
     *
     * Caution:
     * 1. If contract does not have enough tron power to support its votes after unfreezing
     *    this part of frozen balance, the operation will auto clear votes and extract
     *    reward to contract allowance.
     */
    function unfreezeBalance(address payable receiver, uint res) external {
        receiver.unfreeze(res);
    }

    /**
     * @dev Query the timestamp which the specific balance can be unfreezed.
     */
    function queryExpireTime(address payable target, uint res) external view returns(uint) {
        return target.freezeExpireTime(res);
    }

    /**
     * @dev Execute self destruct and transfer all balance and asset of contract to target address.
     *
     * Below situations can cause `revert` excepiton:
     * 1. There are still delegated frozen balance for other account address.
     */
    function killme(address payable target) external {
        selfdestruct(target);
    }
}